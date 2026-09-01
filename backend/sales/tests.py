from datetime import date, datetime, timezone
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import Permission, Role, RolePermission, User

from .models import Customer, CustomerCommunication, Order, OrderItem, OrderStatusHistory, Quotation, QuotationItem


SALES_PERMISSIONS = [
	'MANAGE_CUSTOMERS', 'VIEW_CUSTOMERS', 'MANAGE_CUSTOMER_COMMUNICATION',
	'MANAGE_QUOTATIONS', 'CREATE_SALES_ORDER', 'VIEW_SALES_ORDERS',
	'UPDATE_SALES_ORDER', 'MANAGE_ORDER_STATUS',
]


class SalesTests(APITestCase):
	def setUp(self):
		self.role = Role.objects.create(role_name='Sales Executive', role_code='SALES_EXECUTIVE')
		for code in SALES_PERMISSIONS:
			permission = Permission.objects.get(permission_code=code)
			RolePermission.objects.create(role=self.role, permission=permission)
		self.user = User.objects.create_user(
			email='sales@example.com', password='SecurePassword123!',
			first_name='Sales', last_name='Executive', role=self.role,
		)
		self.customer = Customer.objects.create(
			customer_code='CUS-001', company_name='Acme Industries', contact_person='Asha Shah',
			email='asha@acme.example', phone='1234567890', address='Industrial Area',
			city='Pune', state='Maharashtra', pincode='411001', customer_type=Customer.CustomerType.BUSINESS,
		)

	def order_payload(self, number='SO-001', quotation=None):
		return {
			'order_number': number, 'customer': self.customer, 'quotation': quotation,
			'order_date': '2026-08-20', 'expected_delivery_date': '2026-09-20',
			'priority': 'NORMAL', 'delivery_address': 'Industrial Area', 'delivery_city': 'Pune',
			'delivery_state': 'Maharashtra', 'delivery_pincode': '411001', 'subtotal': '1000.00',
			'tax_amount': '180.00', 'discount_amount': '50.00', 'total_amount': '1130.00',
			'order_status': 'DRAFT', 'notes': 'Test order',
		}

	def quotation_payload(self):
		return {
			'quotation_number': 'QUO-001', 'customer': self.customer, 'quotation_date': date(2026, 8, 20),
			'valid_until': '2026-09-20', 'subtotal': '1000.00', 'tax_amount': '180.00',
			'discount_amount': '50.00', 'total_amount': '1130.00', 'status': 'DRAFT',
		}

	def test_customer_creation_and_duplicate_code_rejection(self):
		self.assertEqual(self.customer.customer_code, 'CUS-001')
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Customer.objects.create(
					customer_code='CUS-001', company_name='Duplicate', contact_person='Contact',
					email='duplicate@example.com', phone='0000000000', address='Address', city='Pune',
					state='Maharashtra', pincode='411001', customer_type=Customer.CustomerType.BUSINESS,
				)

	def test_customer_communication_creation(self):
		communication = CustomerCommunication.objects.create(
			customer=self.customer, communication_type=CustomerCommunication.CommunicationType.CALL,
			subject='Order follow-up', message='Discussed order', communication_date=datetime.now(timezone.utc),
			handled_by=self.user,
		)
		self.assertEqual(communication.handled_by, self.user)

	def test_quotation_creation_and_date_validation(self):
		quotation = Quotation.objects.create(created_by=self.user, **self.quotation_payload())
		self.assertEqual(Decimal(quotation.total_amount), Decimal('1130.00'))
		quotation.valid_until = date(2026, 8, 19)
		with self.assertRaises(ValidationError):
			quotation.full_clean()

	def test_quotation_item_quantity_validation(self):
		quotation = Quotation.objects.create(created_by=self.user, **self.quotation_payload())
		item = QuotationItem(
			quotation=quotation, description='Product A', quantity=Decimal('0'), unit_price=Decimal('100'),
			tax_percentage=Decimal('0'), discount_amount=Decimal('0'), line_total=Decimal('0'),
		)
		with self.assertRaises(ValidationError):
			item.full_clean()

	def test_direct_sales_order_creation(self):
		order = Order.objects.create(created_by=self.user, **self.order_payload())
		self.assertIsNone(order.quotation_id)

	def test_quotation_based_sales_order(self):
		quotation = Quotation.objects.create(created_by=self.user, **self.quotation_payload())
		payload = self.order_payload(number='SO-002')
		payload['quotation'] = quotation
		order = Order.objects.create(created_by=self.user, **payload)
		self.assertEqual(order.quotation_id, quotation.pk)

	def test_duplicate_order_number_rejection(self):
		Order.objects.create(created_by=self.user, **self.order_payload())
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Order.objects.create(created_by=self.user, **self.order_payload())

	def test_order_item_validation(self):
		order = Order.objects.create(created_by=self.user, **self.order_payload())
		item = OrderItem(
			order=order, description='Product A', quantity=Decimal('2'), unit_price=Decimal('-1'),
			tax_percentage=Decimal('0'), discount_amount=Decimal('0'), line_total=Decimal('-2'),
		)
		with self.assertRaises(ValidationError):
			item.full_clean()

	def test_order_status_transition_creates_history(self):
		self.client.force_authenticate(user=self.user)
		order = Order.objects.create(created_by=self.user, **self.order_payload())
		response = self.client.post(reverse('sales-order-change-status', args=[order.pk]), {'new_status': 'PENDING_APPROVAL'}, format='json')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(OrderStatusHistory.objects.get(order=order).new_status, 'PENDING_APPROVAL')

	def test_invalid_order_status_transition_rejected(self):
		self.client.force_authenticate(user=self.user)
		order = Order.objects.create(created_by=self.user, **self.order_payload())
		response = self.client.post(reverse('sales-order-change-status', args=[order.pk]), {'new_status': 'DELIVERED'}, format='json')
		self.assertEqual(response.status_code, 400)

	def test_authentication_requirement(self):
		response = self.client.get(reverse('sales-customer-list'))
		self.assertEqual(response.status_code, 401)

	def test_rbac_permission_enforcement(self):
		self.client.force_authenticate(user=self.user)
		self.role.role_permissions.filter(permission__permission_code='MANAGE_CUSTOMERS').delete()
		response = self.client.post(reverse('sales-customer-list'), {
			'customer_code': 'CUS-002', 'company_name': 'Blocked', 'contact_person': 'Contact',
			'email': 'blocked@example.com', 'phone': '0000000000', 'address': 'Address',
			'city': 'Pune', 'state': 'Maharashtra', 'pincode': '411001', 'customer_type': 'BUSINESS',
		}, format='json')
		self.assertEqual(response.status_code, 403)

# Create your tests here.
