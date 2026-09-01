from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from warehouse.models import Product


class Customer(models.Model):
	class CustomerType(models.TextChoices):
		INDIVIDUAL = 'INDIVIDUAL', 'Individual'
		BUSINESS = 'BUSINESS', 'Business'
		GOVERNMENT = 'GOVERNMENT', 'Government'
		OTHER = 'OTHER', 'Other'

	class Status(models.TextChoices):
		ACTIVE = 'ACTIVE', 'Active'
		INACTIVE = 'INACTIVE', 'Inactive'
		BLOCKED = 'BLOCKED', 'Blocked'

	customer_id = models.BigAutoField(primary_key=True)
	customer_code = models.CharField(max_length=50, unique=True)
	company_name = models.CharField(max_length=200)
	contact_person = models.CharField(max_length=150)
	email = models.EmailField()
	phone = models.CharField(max_length=30)
	alternate_phone = models.CharField(max_length=30, blank=True)
	address = models.TextField()
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	pincode = models.CharField(max_length=20)
	country = models.CharField(max_length=100, default='India')
	customer_type = models.CharField(max_length=20, choices=CustomerType.choices)
	tax_identifier = models.CharField(max_length=100, blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['company_name']
		indexes = [
			models.Index(fields=['company_name']),
			models.Index(fields=['email']),
			models.Index(fields=['phone']),
			models.Index(fields=['status']),
		]

	def __str__(self):
		return f'{self.customer_code} - {self.company_name}'


class CustomerCommunication(models.Model):
	class CommunicationType(models.TextChoices):
		CALL = 'CALL', 'Call'
		EMAIL = 'EMAIL', 'Email'
		MEETING = 'MEETING', 'Meeting'
		WHATSAPP = 'WHATSAPP', 'WhatsApp'
		OTHER = 'OTHER', 'Other'

	class Status(models.TextChoices):
		OPEN = 'OPEN', 'Open'
		FOLLOW_UP = 'FOLLOW_UP', 'Follow Up'
		COMPLETED = 'COMPLETED', 'Completed'
		CANCELLED = 'CANCELLED', 'Cancelled'

	communication_id = models.BigAutoField(primary_key=True)
	customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='communications')
	communication_type = models.CharField(max_length=20, choices=CommunicationType.choices)
	subject = models.CharField(max_length=200)
	message = models.TextField()
	communication_date = models.DateTimeField()
	handled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='customer_communications')
	follow_up_date = models.DateField(null=True, blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-communication_date']
		indexes = [models.Index(fields=['customer', 'status']), models.Index(fields=['follow_up_date'])]

	def __str__(self):
		return f'{self.customer.customer_code} - {self.subject}'


class Quotation(models.Model):
	class Status(models.TextChoices):
		DRAFT = 'DRAFT', 'Draft'
		SENT = 'SENT', 'Sent'
		ACCEPTED = 'ACCEPTED', 'Accepted'
		REJECTED = 'REJECTED', 'Rejected'
		EXPIRED = 'EXPIRED', 'Expired'
		CANCELLED = 'CANCELLED', 'Cancelled'

	quotation_id = models.BigAutoField(primary_key=True)
	quotation_number = models.CharField(max_length=50, unique=True)
	customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='quotations')
	quotation_date = models.DateField()
	valid_until = models.DateField()
	subtotal = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	tax_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	discount_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	total_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
	notes = models.TextField(blank=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_quotations')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-quotation_date']

	def __str__(self):
		return self.quotation_number

	def clean(self):
		if self.valid_until < self.quotation_date:
			raise ValidationError({'valid_until': 'Validity date cannot be before quotation date.'})
		expected_total = self.subtotal + self.tax_amount - self.discount_amount
		if self.total_amount != expected_total:
			raise ValidationError({'total_amount': 'Total must equal subtotal plus tax minus discount.'})


class QuotationItem(models.Model):
	quotation_item_id = models.BigAutoField(primary_key=True)
	quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True, related_name='quotation_items')
	description = models.CharField(max_length=255)
	quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	unit_price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	discount_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	line_total = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['quotation', 'quotation_item_id']

	def __str__(self):
		return f'{self.quotation.quotation_number} - {self.description}'

	def clean(self):
		expected_total = (self.quantity * self.unit_price) + (self.quantity * self.unit_price * self.tax_percentage / 100) - self.discount_amount
		if self.line_total != expected_total:
			raise ValidationError({'line_total': 'Line total does not match quantity, price, tax, and discount.'})


class Order(models.Model):
	class Priority(models.TextChoices):
		LOW = 'LOW', 'Low'
		NORMAL = 'NORMAL', 'Normal'
		HIGH = 'HIGH', 'High'
		URGENT = 'URGENT', 'Urgent'

	class Status(models.TextChoices):
		DRAFT = 'DRAFT', 'Draft'
		PENDING_APPROVAL = 'PENDING_APPROVAL', 'Pending Approval'
		CONFIRMED = 'CONFIRMED', 'Confirmed'
		PROCESSING = 'PROCESSING', 'Processing'
		READY_FOR_DISPATCH = 'READY_FOR_DISPATCH', 'Ready for Dispatch'
		DISPATCHED = 'DISPATCHED', 'Dispatched'
		DELIVERED = 'DELIVERED', 'Delivered'
		CANCELLED = 'CANCELLED', 'Cancelled'
		ON_HOLD = 'ON_HOLD', 'On Hold'

	order_id = models.BigAutoField(primary_key=True)
	order_number = models.CharField(max_length=50, unique=True)
	customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
	quotation = models.ForeignKey(Quotation, on_delete=models.PROTECT, null=True, blank=True, related_name='orders')
	order_date = models.DateField()
	expected_delivery_date = models.DateField(null=True, blank=True)
	priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.NORMAL)
	delivery_address = models.TextField()
	delivery_city = models.CharField(max_length=100)
	delivery_state = models.CharField(max_length=100)
	delivery_pincode = models.CharField(max_length=20)
	subtotal = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	tax_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	discount_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	total_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	order_status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_orders')
	approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='approved_orders')
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-order_date']
		indexes = [models.Index(fields=['order_status', 'order_date']), models.Index(fields=['priority', 'order_status'])]

	def __str__(self):
		return self.order_number

	def clean(self):
		if self.expected_delivery_date and self.expected_delivery_date < self.order_date:
			raise ValidationError({'expected_delivery_date': 'Expected delivery cannot be before order date.'})
		expected_total = self.subtotal + self.tax_amount - self.discount_amount
		if self.total_amount != expected_total:
			raise ValidationError({'total_amount': 'Total must equal subtotal plus tax minus discount.'})


class OrderItem(models.Model):
	order_item_id = models.BigAutoField(primary_key=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True, related_name='order_items')
	description = models.CharField(max_length=255)
	quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	unit_price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	discount_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	line_total = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['order', 'order_item_id']

	def __str__(self):
		return f'{self.order.order_number} - {self.description}'

	def clean(self):
		expected_total = (self.quantity * self.unit_price) + (self.quantity * self.unit_price * self.tax_percentage / 100) - self.discount_amount
		if self.line_total != expected_total:
			raise ValidationError({'line_total': 'Line total does not match quantity, price, tax, and discount.'})


class OrderStatusHistory(models.Model):
	history_id = models.BigAutoField(primary_key=True)
	order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='status_history')
	previous_status = models.CharField(max_length=30, blank=True)
	new_status = models.CharField(max_length=30, choices=Order.Status.choices)
	changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='order_status_changes')
	remarks = models.TextField(blank=True)
	changed_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-changed_at']

	def __str__(self):
		return f'{self.order.order_number}: {self.previous_status} -> {self.new_status}'
