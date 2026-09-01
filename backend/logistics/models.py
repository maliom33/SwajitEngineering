from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from sales.models import Order
from workforce.models import Employee


class Vehicle(models.Model):
	class VehicleType(models.TextChoices):
		TRUCK = 'TRUCK', 'Truck'
		VAN = 'VAN', 'Van'
		PICKUP = 'PICKUP', 'Pickup'
		TEMPO = 'TEMPO', 'Tempo'
		OTHER = 'OTHER', 'Other'

	class FuelType(models.TextChoices):
		DIESEL = 'DIESEL', 'Diesel'
		PETROL = 'PETROL', 'Petrol'
		CNG = 'CNG', 'CNG'
		ELECTRIC = 'ELECTRIC', 'Electric'
		HYBRID = 'HYBRID', 'Hybrid'
		OTHER = 'OTHER', 'Other'

	class Status(models.TextChoices):
		AVAILABLE = 'AVAILABLE', 'Available'
		ASSIGNED = 'ASSIGNED', 'Assigned'
		IN_TRANSIT = 'IN_TRANSIT', 'In Transit'
		UNDER_MAINTENANCE = 'UNDER_MAINTENANCE', 'Under Maintenance'
		INACTIVE = 'INACTIVE', 'Inactive'

	vehicle_id = models.BigAutoField(primary_key=True)
	vehicle_number = models.CharField(max_length=50, unique=True)
	vehicle_type = models.CharField(max_length=20, choices=VehicleType.choices)
	manufacturer = models.CharField(max_length=100, blank=True)
	model = models.CharField(max_length=100, blank=True)
	manufacturing_year = models.PositiveIntegerField(null=True, blank=True)
	capacity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	capacity_unit = models.CharField(max_length=20)
	fuel_type = models.CharField(max_length=20, choices=FuelType.choices)
	registration_date = models.DateField()
	registration_expiry = models.DateField(null=True, blank=True)
	insurance_expiry = models.DateField(null=True, blank=True)
	pollution_certificate_expiry = models.DateField(null=True, blank=True)
	status = models.CharField(max_length=25, choices=Status.choices, default=Status.AVAILABLE)
	current_odometer = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['vehicle_number']
		indexes = [models.Index(fields=['status', 'vehicle_type'])]

	def __str__(self):
		return self.vehicle_number


class Driver(models.Model):
	class AvailabilityStatus(models.TextChoices):
		AVAILABLE = 'AVAILABLE', 'Available'
		ASSIGNED = 'ASSIGNED', 'Assigned'
		ON_DELIVERY = 'ON_DELIVERY', 'On Delivery'
		ON_LEAVE = 'ON_LEAVE', 'On Leave'
		UNAVAILABLE = 'UNAVAILABLE', 'Unavailable'
		SUSPENDED = 'SUSPENDED', 'Suspended'

	driver_id = models.BigAutoField(primary_key=True)
	employee = models.OneToOneField(Employee, on_delete=models.PROTECT, related_name='driver_profile')
	license_number = models.CharField(max_length=100, unique=True)
	license_type = models.CharField(max_length=50)
	license_issue_date = models.DateField()
	license_expiry = models.DateField()
	availability_status = models.CharField(max_length=20, choices=AvailabilityStatus.choices, default=AvailabilityStatus.AVAILABLE)
	emergency_contact_name = models.CharField(max_length=150, blank=True)
	emergency_contact_phone = models.CharField(max_length=30, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['employee__last_name', 'employee__first_name']
		indexes = [models.Index(fields=['availability_status'])]

	def __str__(self):
		return f'{self.employee.employee_code} - {self.license_number}'

	def clean(self):
		if self.license_expiry < self.license_issue_date:
			raise ValidationError({'license_expiry': 'License expiry cannot be before issue date.'})


class VehicleMaintenance(models.Model):
	class MaintenanceType(models.TextChoices):
		ROUTINE_SERVICE = 'ROUTINE_SERVICE', 'Routine Service'
		REPAIR = 'REPAIR', 'Repair'
		INSPECTION = 'INSPECTION', 'Inspection'
		TYRE_CHANGE = 'TYRE_CHANGE', 'Tyre Change'
		OIL_CHANGE = 'OIL_CHANGE', 'Oil Change'
		OTHER = 'OTHER', 'Other'

	class Status(models.TextChoices):
		SCHEDULED = 'SCHEDULED', 'Scheduled'
		IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
		COMPLETED = 'COMPLETED', 'Completed'
		CANCELLED = 'CANCELLED', 'Cancelled'

	maintenance_id = models.BigAutoField(primary_key=True)
	vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name='maintenance_records')
	maintenance_type = models.CharField(max_length=30, choices=MaintenanceType.choices)
	service_date = models.DateField()
	next_service_date = models.DateField(null=True, blank=True)
	odometer_reading = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	cost = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	description = models.TextField()
	service_provider = models.CharField(max_length=150, blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='vehicle_maintenance_records')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.vehicle.vehicle_number} - {self.service_date}'


class Route(models.Model):
	class Algorithm(models.TextChoices):
		DIJKSTRA = 'DIJKSTRA', 'Dijkstra'
		A_STAR = 'A_STAR', 'A*'
		SHORTEST_PATH = 'SHORTEST_PATH', 'Shortest Path'
		MANUAL = 'MANUAL', 'Manual'
		OTHER = 'OTHER', 'Other'

	class Status(models.TextChoices):
		PLANNED = 'PLANNED', 'Planned'
		OPTIMIZED = 'OPTIMIZED', 'Optimized'
		ASSIGNED = 'ASSIGNED', 'Assigned'
		IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
		COMPLETED = 'COMPLETED', 'Completed'
		CANCELLED = 'CANCELLED', 'Cancelled'

	route_id = models.BigAutoField(primary_key=True)
	route_number = models.CharField(max_length=50, unique=True)
	origin_address = models.TextField()
	origin_city = models.CharField(max_length=100)
	origin_state = models.CharField(max_length=100)
	origin_pincode = models.CharField(max_length=20)
	destination_address = models.TextField()
	destination_city = models.CharField(max_length=100)
	destination_state = models.CharField(max_length=100)
	destination_pincode = models.CharField(max_length=20)
	distance_km = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	estimated_duration_minutes = models.PositiveIntegerField()
	route_algorithm = models.CharField(max_length=30, choices=Algorithm.choices, default=Algorithm.MANUAL)
	route_status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
	planned_start_time = models.DateTimeField(null=True, blank=True)
	planned_end_time = models.DateTimeField(null=True, blank=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_routes')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
		indexes = [models.Index(fields=['route_status']), models.Index(fields=['origin_city', 'destination_city'])]

	def __str__(self):
		return self.route_number

	def clean(self):
		if self.planned_start_time and self.planned_end_time and self.planned_end_time < self.planned_start_time:
			raise ValidationError({'planned_end_time': 'Planned end cannot be before planned start.'})


class Delivery(models.Model):
	class Status(models.TextChoices):
		CREATED = 'CREATED', 'Created'
		ASSIGNED = 'ASSIGNED', 'Assigned'
		PICKED_UP = 'PICKED_UP', 'Picked Up'
		IN_TRANSIT = 'IN_TRANSIT', 'In Transit'
		OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY', 'Out for Delivery'
		DELIVERED = 'DELIVERED', 'Delivered'
		FAILED = 'FAILED', 'Failed'
		CANCELLED = 'CANCELLED', 'Cancelled'
		ON_HOLD = 'ON_HOLD', 'On Hold'

	delivery_id = models.BigAutoField(primary_key=True)
	delivery_number = models.CharField(max_length=50, unique=True)
	order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='deliveries')
	driver = models.ForeignKey(Driver, on_delete=models.PROTECT, null=True, blank=True, related_name='deliveries')
	vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, null=True, blank=True, related_name='deliveries')
	route = models.ForeignKey(Route, on_delete=models.PROTECT, null=True, blank=True, related_name='deliveries')
	assigned_at = models.DateTimeField(null=True, blank=True)
	pickup_time = models.DateTimeField(null=True, blank=True)
	expected_delivery_time = models.DateTimeField(null=True, blank=True)
	actual_delivery_time = models.DateTimeField(null=True, blank=True)
	delivery_status = models.CharField(max_length=25, choices=Status.choices, default=Status.CREATED)
	delivery_notes = models.TextField(blank=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_deliveries')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
		constraints = [models.UniqueConstraint(fields=['order'], condition=models.Q(delivery_status__in=['CREATED', 'ASSIGNED', 'PICKED_UP', 'IN_TRANSIT', 'OUT_FOR_DELIVERY']), name='one_active_delivery_per_order')]
		indexes = [models.Index(fields=['delivery_status']), models.Index(fields=['driver', 'delivery_status']), models.Index(fields=['vehicle', 'delivery_status']), models.Index(fields=['order'])]

	def __str__(self):
		return self.delivery_number


class DeliveryStatusHistory(models.Model):
	status_history_id = models.BigAutoField(primary_key=True)
	delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT, related_name='status_history')
	previous_status = models.CharField(max_length=25, blank=True)
	new_status = models.CharField(max_length=25, choices=Delivery.Status.choices)
	changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='delivery_status_changes')
	location_description = models.CharField(max_length=255, blank=True)
	remarks = models.TextField(blank=True)
	changed_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-changed_at']

	def __str__(self):
		return f'{self.delivery.delivery_number}: {self.previous_status} -> {self.new_status}'
