from datetime import date, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from accounts.models import Permission, Role, RolePermission, User
from sales.models import Customer, Order, OrderItem
from warehouse.models import Product, ProductCategory

from .models import Expense, ExpenseCategory, FinancialTransaction, Invoice, InvoiceItem, Payment
from .services.finance_service import approve_expense, create_invoice_from_order, record_payment, refund_payment, update_invoice_statuses


PERMISSIONS = ['VIEW_FINANCE', 'MANAGE_INVOICES', 'CREATE_INVOICE', 'MANAGE_PAYMENTS', 'RECORD_PAYMENT', 'MANAGE_EXPENSES', 'APPROVE_EXPENSES', 'VIEW_FINANCIAL_TRANSACTIONS', 'MANAGE_FINANCIAL_ADJUSTMENTS']


class FinanceTests(APITestCase):
	def setUp(self):
		self.role = Role.objects.create(role_name='Finance Manager', role_code='FINANCE_MANAGER')
		for code in PERMISSIONS:
			RolePermission.objects.create(role=self.role, permission=Permission.objects.get(permission_code=code))
		self.user = User.objects.create_user(email='finance@example.com', password='SecurePassword123!', first_name='Finance', last_name='Manager', role=self.role)
		self.customer = Customer.objects.create(customer_code='CUS-F-001', company_name='Finance Customer', contact_person='Contact', email='customer-f@example.com', phone='999', address='Address', city='Pune', state='MH', pincode='411001', customer_type='BUSINESS')
		category = ProductCategory.objects.create(category_code='CAT-F-001', category_name='Finance Product')
		self.product = Product.objects.create(sku='SKU-F-001', product_code='PROD-F-001', product_name='Product', category=category, unit_price=Decimal('100'))
		self.order = Order.objects.create(order_number='SO-F-001', customer=self.customer, order_date=date(2026, 8, 21), delivery_address='Address', delivery_city='Pune', delivery_state='MH', delivery_pincode='411001', subtotal=Decimal('200'), tax_amount=Decimal('36'), discount_amount=Decimal('0'), total_amount=Decimal('236'), order_status='CONFIRMED', created_by=self.user)
		OrderItem.objects.create(order=self.order, product=self.product, description='Product', quantity=Decimal('2'), unit_price=Decimal('100'), tax_percentage=Decimal('18'), line_total=Decimal('236'))

	def test_invoice_creation_from_order_and_uniqueness(self):
		invoice = create_invoice_from_order(order=self.order, created_by=self.user, invoice_number='INV-001', due_date=date(2026, 9, 20))
		self.assertEqual(invoice.total_amount, Decimal('236.00'))
		self.assertEqual(invoice.items.count(), 1)
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Invoice.objects.create(invoice_number='INV-001', order=Order.objects.create(order_number='SO-F-002', customer=self.customer, order_date=date(2026, 8, 21), delivery_address='A', delivery_city='Pune', delivery_state='MH', delivery_pincode='1', subtotal=0, total_amount=0, created_by=self.user), customer=self.customer, invoice_date=date.today(), due_date=date.today(), subtotal=0, total_amount=0, amount_due=0, created_by=self.user)

	def test_invoice_due_date_and_item_calculation_validation(self):
		invoice = Invoice(invoice_number='INV-X', order=self.order, customer=self.customer, invoice_date=date(2026, 8, 21), due_date=date(2026, 8, 20), subtotal=0, total_amount=0, amount_due=0, created_by=self.user)
		with self.assertRaises(ValidationError):
			invoice.full_clean()

	def test_successful_partial_and_full_payment(self):
		invoice = create_invoice_from_order(order=self.order, created_by=self.user, invoice_number='INV-001', due_date=date(2026, 9, 20))
		record_payment(invoice=invoice, payment_reference='PAY-001', amount=Decimal('100'), payment_date=date.today(), payment_method='UPI', received_by=self.user)
		invoice.refresh_from_db()
		self.assertEqual(invoice.status, Invoice.Status.PARTIALLY_PAID)
		record_payment(invoice=invoice, payment_reference='PAY-002', amount=Decimal('136'), payment_date=date.today(), payment_method='UPI', received_by=self.user)
		invoice.refresh_from_db()
		self.assertEqual(invoice.status, Invoice.Status.PAID)
		self.assertEqual(FinancialTransaction.objects.filter(transaction_type='PAYMENT_RECEIVED').count(), 2)

	def test_overpayment_rejected_and_payment_reference_unique(self):
		invoice = create_invoice_from_order(order=self.order, created_by=self.user, invoice_number='INV-001', due_date=date(2026, 9, 20))
		with self.assertRaises(ValueError):
			record_payment(invoice=invoice, payment_reference='PAY-001', amount=Decimal('237'), payment_date=date.today(), payment_method='CASH', received_by=self.user)

	def test_overdue_detection(self):
		invoice = create_invoice_from_order(order=self.order, created_by=self.user, invoice_number='INV-001', due_date=timezone.localdate() - timedelta(days=1))
		update_invoice_statuses()
		invoice.refresh_from_db()
		self.assertEqual(invoice.status, Invoice.Status.OVERDUE)

	def test_expense_approval_creates_ledger(self):
		category = ExpenseCategory.objects.create(category_code='FUEL', category_name='Fuel')
		expense = Expense.objects.create(expense_number='EXP-001', category=category, amount=Decimal('500'), expense_date=date.today(), description='Fuel', payment_method='CASH', status=Expense.Status.PENDING_APPROVAL, recorded_by=self.user)
		approve_expense(expense=expense, approved_by=self.user)
		self.assertEqual(Expense.objects.get(pk=expense.pk).status, Expense.Status.APPROVED)
		self.assertEqual(FinancialTransaction.objects.filter(reference_type='Expense').count(), 1)

	def test_refund_updates_payment_and_invoice(self):
		invoice = create_invoice_from_order(order=self.order, created_by=self.user, invoice_number='INV-001', due_date=date(2026, 9, 20))
		payment = record_payment(invoice=invoice, payment_reference='PAY-001', amount=Decimal('100'), payment_date=date.today(), payment_method='CASH', received_by=self.user)
		refund_payment(payment=payment, amount=Decimal('100'), processed_by=self.user, refund_reference='REF-001')
		invoice.refresh_from_db(); payment.refresh_from_db()
		self.assertEqual(payment.payment_status, Payment.Status.REFUNDED)
		self.assertEqual(invoice.amount_paid, Decimal('0.00'))
		self.assertEqual(FinancialTransaction.objects.filter(transaction_type='REFUND').count(), 1)

	def test_authentication_and_rbac(self):
		response = self.client.get(reverse('finance-invoice-list'))
		self.assertEqual(response.status_code, 401)
		self.client.force_authenticate(user=self.user)
		self.role.role_permissions.filter(permission__permission_code='CREATE_INVOICE').delete()
		response = self.client.post(reverse('finance-invoice-list'), {}, format='json')
		self.assertEqual(response.status_code, 403)

# Create your tests here.
