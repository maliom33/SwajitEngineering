from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import Permission, Role, RolePermission, User
from logistics.models import Delivery, Driver, Vehicle
from sales.models import Customer, Order
from warehouse.models import Inventory, Product, ProductCategory, StockReservation, StockReservationItem, Warehouse
from workforce.models import Department, Designation, Employee

from .models import DeliveryChallan, Dispatch, DispatchItem, DispatchStatusHistory
from .services.dispatch_service import cancel_dispatch, confirm_dispatch, create_dispatch, generate_delivery_challan, handover_dispatch, prepare_dispatch


PERMISSIONS = ['MANAGE_DISPATCH', 'VIEW_DISPATCH', 'CREATE_DISPATCH', 'PREPARE_DISPATCH', 'GENERATE_DELIVERY_CHALLAN', 'HANDOVER_DISPATCH', 'UPDATE_DISPATCH_STATUS', 'VIEW_DISPATCH_HISTORY']


class DispatchTests(APITestCase):
	def setUp(self):
		self.role = Role.objects.create(role_name='Dispatch Executive', role_code='DISPATCH_EXECUTIVE')
		for code in PERMISSIONS:
			RolePermission.objects.create(role=self.role, permission=Permission.objects.get(permission_code=code))
		self.user = User.objects.create_user(email='dispatch@example.com', password='SecurePassword123!', first_name='Dispatch', last_name='Executive', role=self.role)
		department = Department.objects.create(department_name='Dispatch')
		designation = Designation.objects.create(designation_name='Dispatch Executive')
		employee = Employee.objects.create(user=self.user, employee_code='EMP-D-001', first_name='Driver', last_name='One', email='driver@example.com', phone='123', department=department, designation=designation, joining_date=date(2026, 1, 1), employment_type='FULL_TIME', base_salary=Decimal('40000'))
		self.driver = Driver.objects.create(employee=employee, license_number='LIC-D-001', license_type='LMV', license_issue_date=date(2024, 1, 1), license_expiry=date(2030, 1, 1))
		self.vehicle = Vehicle.objects.create(vehicle_number='MH-D-0001', vehicle_type='VAN', capacity=Decimal('1000'), capacity_unit='KG', fuel_type='DIESEL', registration_date=date(2024, 1, 1))
		self.warehouse = Warehouse.objects.create(warehouse_code='WH-D-001', warehouse_name='Dispatch Warehouse', location='Pune', address='Road', city='Pune', state='MH', pincode='411001', contact_number='123', manager=employee)
		category = ProductCategory.objects.create(category_code='CAT-D-001', category_name='Dispatch Product')
		self.product = Product.objects.create(sku='SKU-D-001', product_code='PROD-D-001', product_name='Product', category=category, unit_price=Decimal('10'))
		customer = Customer.objects.create(customer_code='CUS-D-001', company_name='Customer', contact_person='Contact', email='customer-d@example.com', phone='999', address='Delivery Address', city='Mumbai', state='MH', pincode='400001', customer_type='BUSINESS')
		self.order = Order.objects.create(order_number='SO-D-001', customer=customer, order_date=date(2026, 8, 20), delivery_address='Delivery Address', delivery_city='Mumbai', delivery_state='MH', delivery_pincode='400001', subtotal=Decimal('100'), total_amount=Decimal('100'), order_status='READY_FOR_DISPATCH', created_by=self.user)
		self.delivery = Delivery.objects.create(delivery_number='DEL-D-001', order=self.order, driver=self.driver, vehicle=self.vehicle, created_by=self.user)
		reservation = StockReservation.objects.create(order=self.order, warehouse=self.warehouse, status='ALLOCATED', reserved_by=self.user)
		StockReservationItem.objects.create(reservation=reservation, product=self.product, quantity=Decimal('10'))

	def test_dispatch_creation_requires_ready_order_and_prevents_duplicate(self):
		dispatch = create_dispatch(order=self.order, delivery=self.delivery, warehouse=self.warehouse, dispatch_number='DSP-001', prepared_by=self.user, scheduled_dispatch_date=date(2026, 8, 20))
		self.assertEqual(dispatch.dispatch_status, Dispatch.Status.SCHEDULED)
		with self.assertRaises(ValueError):
			create_dispatch(order=self.order, delivery=self.delivery, warehouse=self.warehouse, dispatch_number='DSP-002', prepared_by=self.user, scheduled_dispatch_date=date(2026, 8, 20))

	def test_dispatch_item_quantity_and_preparation(self):
		dispatch = create_dispatch(order=self.order, delivery=self.delivery, warehouse=self.warehouse, dispatch_number='DSP-001', prepared_by=self.user, scheduled_dispatch_date=date(2026, 8, 20))
		with self.assertRaises(ValueError):
			prepare_dispatch(dispatch, items=[{'product': self.product.pk, 'quantity': '11', 'package_count': 1}], changed_by=self.user)
		prepare_dispatch(dispatch, items=[{'product': self.product.pk, 'quantity': '10', 'package_count': 2}], changed_by=self.user)
		self.assertEqual(dispatch.__class__.objects.get(pk=dispatch.pk).dispatch_status, Dispatch.Status.READY)

	def prepared_dispatch(self):
		dispatch = create_dispatch(order=self.order, delivery=self.delivery, warehouse=self.warehouse, dispatch_number='DSP-001', prepared_by=self.user, scheduled_dispatch_date=date(2026, 8, 20))
		prepare_dispatch(dispatch, items=[{'product': self.product.pk, 'quantity': '10', 'package_count': 2}], changed_by=self.user)
		return dispatch

	def test_challan_snapshots_delivery_driver_vehicle(self):
		dispatch = self.prepared_dispatch()
		challan = generate_delivery_challan(dispatch, issued_by=self.user, challan_number='DC-001')
		self.assertEqual(challan.vehicle_number_snapshot, self.vehicle.vehicle_number)
		self.assertEqual(challan.driver_name_snapshot, 'Driver One')
		self.assertEqual(challan.total_quantity, Decimal('10'))
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				DeliveryChallan.objects.create(challan_number='DC-001', dispatch=dispatch, challan_date=date.today(), issued_by=self.user, vehicle_number_snapshot='x', driver_name_snapshot='x', delivery_address='x')

	def test_handover_confirmation_and_history(self):
		dispatch = self.prepared_dispatch()
		generate_delivery_challan(dispatch, issued_by=self.user, challan_number='DC-001')
		handover_dispatch(dispatch, handed_over_by=self.user)
		confirm_dispatch(dispatch, confirmed_by=self.user)
		dispatch.refresh_from_db(); self.delivery.refresh_from_db()
		self.assertEqual(dispatch.dispatch_status, Dispatch.Status.DISPATCHED)
		self.assertEqual(self.delivery.delivery_status, 'IN_TRANSIT')
		self.assertEqual(DispatchStatusHistory.objects.filter(dispatch=dispatch).count(), 4)

	def test_invalid_transition_and_cancellation(self):
		dispatch = self.prepared_dispatch()
		with self.assertRaises(ValueError):
			confirm_dispatch(dispatch, confirmed_by=self.user)
		cancel_dispatch(dispatch, cancelled_by=self.user, remarks='Cancelled')
		self.assertEqual(Dispatch.objects.get(pk=dispatch.pk).dispatch_status, Dispatch.Status.CANCELLED)

	def test_authentication_and_rbac(self):
		response = self.client.get(reverse('dispatch-record-list'))
		self.assertEqual(response.status_code, 401)
		self.client.force_authenticate(user=self.user)
		self.role.role_permissions.filter(permission__permission_code='CREATE_DISPATCH').delete()
		response = self.client.post(reverse('dispatch-record-list'), {}, format='json')
		self.assertEqual(response.status_code, 403)

# Create your tests here.
