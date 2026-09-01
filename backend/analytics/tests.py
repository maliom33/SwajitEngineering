from datetime import date
from decimal import Decimal

from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import Permission, Role, RolePermission, User
from sales.models import Customer, Order


class AnalyticsTests(APITestCase):
	def setUp(self):
		self.role = Role.objects.create(role_name='Director', role_code='DIRECTOR')
		for code in ['VIEW_ANALYTICS', 'VIEW_EXECUTIVE_DASHBOARD', 'VIEW_SALES_ANALYTICS']:
			RolePermission.objects.create(role=self.role, permission=Permission.objects.get(permission_code=code))
		self.user = User.objects.create_user(email='director@example.com', password='SecurePassword123!', first_name='Director', last_name='User', role=self.role)
		self.customer = Customer.objects.create(customer_code='CUS-A-001', company_name='Analytics Customer', contact_person='Contact', email='analytics@example.com', phone='999', address='Address', city='Pune', state='MH', pincode='411001', customer_type='BUSINESS')
		Order.objects.create(order_number='SO-A-001', customer=self.customer, order_date=date(2026, 8, 21), delivery_address='Address', delivery_city='Pune', delivery_state='MH', delivery_pincode='411001', subtotal=Decimal('100'), tax_amount=Decimal('18'), total_amount=Decimal('118'), order_status='DELIVERED', created_by=self.user)

	def test_executive_dashboard_and_sales_response_shape(self):
		self.client.force_authenticate(user=self.user)
		dashboard = self.client.get(reverse('analytics-executive-dashboard'))
		self.assertEqual(dashboard.status_code, 200)
		self.assertTrue(dashboard.data['success'])
		self.assertIn('sales', dashboard.data['data'])
		sales = self.client.get(reverse('analytics-sales'), {'start_date': '2026-08-01', 'end_date': '2026-08-31'})
		self.assertEqual(sales.status_code, 200)
		self.assertEqual(sales.data['data']['total_orders'], 1)

	def test_invalid_date_range(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.get(reverse('analytics-sales'), {'start_date': '2026-09-01', 'end_date': '2026-08-01'})
		self.assertEqual(response.status_code, 400)
		self.assertFalse(response.data['success'])

	def test_empty_module_data_is_zero_safe(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.get(reverse('analytics-workforce'))
		self.assertEqual(response.status_code, 403)
		response = self.client.get(reverse('analytics-kpis'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['data']['delivery_completion_rate'], Decimal('0'))

	def test_authentication_and_read_only_access(self):
		response = self.client.get(reverse('analytics-kpis'))
		self.assertEqual(response.status_code, 401)
		self.client.force_authenticate(user=self.user)
		response = self.client.post(reverse('analytics-kpis'), {}, format='json')
		self.assertEqual(response.status_code, 405)

# Create your tests here.
