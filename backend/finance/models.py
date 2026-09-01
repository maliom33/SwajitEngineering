from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from sales.models import Customer, Order
from warehouse.models import Product


class Invoice(models.Model):
	class Status(models.TextChoices):
		DRAFT = 'DRAFT', 'Draft'
		ISSUED = 'ISSUED', 'Issued'
		PARTIALLY_PAID = 'PARTIALLY_PAID', 'Partially Paid'
		PAID = 'PAID', 'Paid'
		OVERDUE = 'OVERDUE', 'Overdue'
		CANCELLED = 'CANCELLED', 'Cancelled'
		VOID = 'VOID', 'Void'

	invoice_id = models.BigAutoField(primary_key=True)
	invoice_number = models.CharField(max_length=50, unique=True)
	order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name='invoice')
	customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='invoices')
	invoice_date = models.DateField()
	due_date = models.DateField()
	subtotal = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	tax_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	discount_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	total_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	amount_paid = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	amount_due = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	currency = models.CharField(max_length=3, default='INR')
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_invoices')
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-invoice_date']
		indexes = [models.Index(fields=['status', 'due_date']), models.Index(fields=['customer']), models.Index(fields=['order'])]

	def __str__(self):
		return self.invoice_number

	def clean(self):
		if self.due_date < self.invoice_date:
			raise ValidationError({'due_date': 'Due date cannot be before invoice date.'})
		expected_total = self.subtotal + self.tax_amount - self.discount_amount
		if self.total_amount != expected_total:
			raise ValidationError({'total_amount': 'Total must equal subtotal plus tax minus discount.'})
		if self.amount_paid > self.total_amount:
			raise ValidationError({'amount_paid': 'Amount paid cannot exceed total amount.'})
		if self.amount_due != self.total_amount - self.amount_paid:
			raise ValidationError({'amount_due': 'Amount due must equal total minus amount paid.'})


class InvoiceItem(models.Model):
	invoice_item_id = models.BigAutoField(primary_key=True)
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True, related_name='invoice_items')
	description = models.CharField(max_length=255)
	quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	unit_price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	discount_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	line_total = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.invoice.invoice_number} - {self.description}'

	def clean(self):
		expected = self.quantity * self.unit_price + self.quantity * self.unit_price * self.tax_percentage / 100 - self.discount_amount
		if self.line_total != expected:
			raise ValidationError({'line_total': 'Line total does not match item values.'})


class Payment(models.Model):
	class Method(models.TextChoices):
		CASH = 'CASH', 'Cash'
		BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer'
		UPI = 'UPI', 'UPI'
		CARD = 'CARD', 'Card'
		CHEQUE = 'CHEQUE', 'Cheque'
		OTHER = 'OTHER', 'Other'

	class Status(models.TextChoices):
		PENDING = 'PENDING', 'Pending'
		SUCCESS = 'SUCCESS', 'Success'
		FAILED = 'FAILED', 'Failed'
		REFUNDED = 'REFUNDED', 'Refunded'
		CANCELLED = 'CANCELLED', 'Cancelled'

	payment_id = models.BigAutoField(primary_key=True)
	payment_reference = models.CharField(max_length=100, unique=True)
	invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='payments')
	payment_date = models.DateField()
	amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	payment_method = models.CharField(max_length=20, choices=Method.choices)
	payment_status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	transaction_reference = models.CharField(max_length=150, blank=True)
	received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='received_payments')
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-payment_date']
		indexes = [models.Index(fields=['payment_status', 'payment_date']), models.Index(fields=['invoice'])]

	def __str__(self):
		return self.payment_reference


class ExpenseCategory(models.Model):
	category_id = models.BigAutoField(primary_key=True)
	category_code = models.CharField(max_length=50, unique=True)
	category_name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.category_name


class Expense(models.Model):
	class Method(models.TextChoices):
		CASH = 'CASH', 'Cash'
		BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer'
		UPI = 'UPI', 'UPI'
		CARD = 'CARD', 'Card'
		CHEQUE = 'CHEQUE', 'Cheque'
		OTHER = 'OTHER', 'Other'

	class Status(models.TextChoices):
		DRAFT = 'DRAFT', 'Draft'
		PENDING_APPROVAL = 'PENDING_APPROVAL', 'Pending Approval'
		APPROVED = 'APPROVED', 'Approved'
		REJECTED = 'REJECTED', 'Rejected'
		PAID = 'PAID', 'Paid'
		CANCELLED = 'CANCELLED', 'Cancelled'

	expense_id = models.BigAutoField(primary_key=True)
	expense_number = models.CharField(max_length=50, unique=True)
	category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT, related_name='expenses')
	amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	expense_date = models.DateField()
	description = models.TextField()
	vendor_name = models.CharField(max_length=200, blank=True)
	payment_method = models.CharField(max_length=20, choices=Method.choices)
	payment_reference = models.CharField(max_length=150, blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
	recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='recorded_expenses')
	approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='approved_expenses')
	receipt_file = models.FileField(upload_to='finance/receipts/', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-expense_date']
		indexes = [models.Index(fields=['category', 'expense_date']), models.Index(fields=['status', 'expense_date'])]

	def __str__(self):
		return self.expense_number


class FinancialTransaction(models.Model):
	class Type(models.TextChoices):
		REVENUE = 'REVENUE', 'Revenue'
		EXPENSE = 'EXPENSE', 'Expense'
		PAYMENT_RECEIVED = 'PAYMENT_RECEIVED', 'Payment Received'
		REFUND = 'REFUND', 'Refund'
		ADJUSTMENT = 'ADJUSTMENT', 'Adjustment'

	transaction_id = models.BigAutoField(primary_key=True)
	transaction_number = models.CharField(max_length=100, unique=True)
	transaction_type = models.CharField(max_length=25, choices=Type.choices)
	transaction_date = models.DateTimeField(auto_now_add=True)
	amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	reference_type = models.CharField(max_length=50)
	reference_id = models.CharField(max_length=100)
	description = models.TextField()
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='financial_transactions')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-transaction_date']
		indexes = [models.Index(fields=['transaction_type', 'transaction_date']), models.Index(fields=['reference_type', 'reference_id'])]

	def __str__(self):
		return self.transaction_number


class Refund(models.Model):
	refund_id = models.BigAutoField(primary_key=True)
	payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name='refunds')
	refund_reference = models.CharField(max_length=100, unique=True)
	amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	refund_date = models.DateField()
	processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='processed_refunds')
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.refund_reference
