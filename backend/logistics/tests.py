from datetime import date, datetime, timezone
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import Permission, Role, RolePermission, User
from sales.models import Customer, Order
from workforce.models import Department, Designation, Employee

from .models import Delivery, DeliveryStatusHistory, Driver, Route, Vehicle, VehicleMaintenance
from .services.delivery_service import assign_delivery, create_delivery, update_delivery_status


PERMISSIONS = ['MANAGE_VEHICLES', 'MANAGE_DRIVERS', 'VIEW_FLEET', 'MANAGE_VEHICLE_MAINTENANCE', 'MANAGE_ROUTES', 'MANAGE_DELIVERIES', 'ASSIGN_DELIVERIES', 'UPDATE_DELIVERY_STATUS', 'VIEW_DELIVERY_TRACKING']


class LogisticsTests(APITestCase):
	def setUp(self):
		self.role = Role.objects.create(role_name='Logistics Manager', role_code='LOGISTICS_MANAGER')
		for code in PERMISSIONS:
			RolePermission.objects.create(role=self.role, permission=Permission.objects.get(permission_code=code))
		self.user = User.objects.create_user(email='logistics@example.com', password='SecurePassword123!', first_name='Logistics', last_name='Manager', role=self.role)
		department = Department.objects.create(department_name='Logistics')
		designation = Designation.objects.create(designation_name='Driver')
		self.employee = Employee.objects.create(user=self.user, employee_code='EMP-L-001', first_name='Driver', last_name='One', email='driver@example.com', phone='1234567890', department=department, designation=designation, joining_date=date(2026, 1, 1), employment_type=Employee.EmploymentType.FULL_TIME, base_salary=Decimal('40000'))
		self.driver = Driver.objects.create(employee=self.employee, license_number='LIC-001', license_type='LMV', license_issue_date=date(2024, 1, 1), license_expiry=date(2030, 1, 1))
		self.vehicle = Vehicle.objects.create(vehicle_number='MH-01-AA-0001', vehicle_type=Vehicle.VehicleType.VAN, capacity=Decimal('1000'), capacity_unit='KG', fuel_type=Vehicle.FuelType.DIESEL, registration_date=date(2024, 1, 1))
		self.route = Route.objects.create(route_number='R-001', origin_address='Origin', origin_city='Pune', origin_state='MH', origin_pincode='411001', destination_address='Destination', destination_city='Mumbai', destination_state='MH', destination_pincode='400001', distance_km=Decimal('150'), estimated_duration_minutes=240, created_by=self.user)
		customer = Customer.objects.create(customer_code='CUS-L-001', company_name='Customer', contact_person='Contact', email='customer@example.com', phone='9999999999', address='Address', city='Pune', state='MH', pincode='411001', customer_type=Customer.CustomerType.BUSINESS)
		self.order = Order.objects.create(order_number='SO-L-001', customer=customer, order_date=date(2026, 8, 20), delivery_address='Address', delivery_city='Mumbai', delivery_state='MH', delivery_pincode='400001', subtotal=Decimal('100'), total_amount=Decimal('100'), order_status='READY_FOR_DISPATCH', created_by=self.user)

	def test_vehicle_driver_maintenance_and_route_creation(self):
		self.assertEqual(self.vehicle.vehicle_number, 'MH-01-AA-0001')
		self.assertEqual(self.driver.employee, self.employee)
		maintenance = VehicleMaintenance.objects.create(vehicle=self.vehicle, maintenance_type='INSPECTION', service_date=date(2026, 8, 20), odometer_reading=Decimal('100'), cost=Decimal('500'), description='Inspection', created_by=self.user)
		self.assertEqual(maintenance.vehicle, self.vehicle)

	def test_duplicate_vehicle_and_license_rejected(self):
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Vehicle.objects.create(vehicle_number=self.vehicle.vehicle_number, vehicle_type='VAN', capacity=1, capacity_unit='KG', fuel_type='DIESEL', registration_date=date(2024, 1, 1))
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Driver.objects.create(employee=Employee.objects.create(employee_code='EMP-L-002', first_name='Two', last_name='Driver', email='two@example.com', phone='1', department=self.employee.department, designation=self.employee.designation, joining_date=date(2026, 1, 1), employment_type='FULL_TIME', base_salary=1), license_number='LIC-001', license_type='LMV', license_issue_date=date(2024, 1, 1), license_expiry=date(2030, 1, 1))

	def test_delivery_creation_and_duplicate_active_prevention(self):
		delivery = create_delivery(order=self.order, delivery_number='DEL-001', created_by=self.user, route=self.route)
		self.assertEqual(delivery.delivery_status, Delivery.Status.CREATED)
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Delivery.objects.create(delivery_number='DEL-002', order=self.order, created_by=self.user)

	def test_assignment_rejects_unavailable_driver_or_vehicle(self):
		delivery = create_delivery(order=self.order, delivery_number='DEL-001', created_by=self.user)
		self.driver.availability_status = Driver.AvailabilityStatus.ON_DELIVERY
		self.driver.save(update_fields=['availability_status'])
		with self.assertRaises(ValueError):
			assign_delivery(delivery, driver=self.driver, vehicle=self.vehicle, changed_by=self.user)

	def test_assignment_and_status_updates_history_and_assets(self):
		delivery = create_delivery(order=self.order, delivery_number='DEL-001', created_by=self.user, route=self.route)
		assign_delivery(delivery, driver=self.driver, vehicle=self.vehicle, changed_by=self.user)
		update_delivery_status(delivery, new_status='PICKED_UP', changed_by=self.user)
		update_delivery_status(delivery, new_status='IN_TRANSIT', changed_by=self.user)
		update_delivery_status(delivery, new_status='OUT_FOR_DELIVERY', changed_by=self.user)
		update_delivery_status(delivery, new_status='DELIVERED', changed_by=self.user)
		self.driver.refresh_from_db(); self.vehicle.refresh_from_db()
		self.assertEqual(self.driver.availability_status, Driver.AvailabilityStatus.AVAILABLE)
		self.assertEqual(self.vehicle.status, Vehicle.Status.AVAILABLE)
		self.assertEqual(DeliveryStatusHistory.objects.filter(delivery=delivery).count(), 6)

	def test_invalid_status_transition_rejected(self):
		delivery = create_delivery(order=self.order, delivery_number='DEL-001', created_by=self.user)
		with self.assertRaises(ValueError):
			update_delivery_status(delivery, new_status='DELIVERED', changed_by=self.user)

	def test_authentication_and_rbac(self):
		response = self.client.get(reverse('logistics-vehicle-list'))
		self.assertEqual(response.status_code, 401)
		self.client.force_authenticate(user=self.user)
		self.role.role_permissions.filter(permission__permission_code='MANAGE_VEHICLES').delete()
		response = self.client.post(reverse('logistics-vehicle-list'), {'vehicle_number': 'NEW-1', 'vehicle_type': 'VAN', 'capacity': '10', 'capacity_unit': 'KG', 'fuel_type': 'DIESEL', 'registration_date': '2026-01-01'}, format='json')
		self.assertEqual(response.status_code, 403)

# Create your tests here.
