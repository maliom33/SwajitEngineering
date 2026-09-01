from django.contrib import admin

from .models import Delivery, DeliveryStatusHistory, Driver, Route, Vehicle, VehicleMaintenance


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
	list_display = ['vehicle_number', 'vehicle_type', 'status', 'capacity', 'insurance_expiry']
	list_filter = ['vehicle_type', 'fuel_type', 'status']
	search_fields = ['vehicle_number', 'manufacturer', 'model']


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
	list_display = ['employee', 'license_number', 'license_expiry', 'availability_status']
	list_filter = ['availability_status', 'license_type']
	search_fields = ['employee__employee_code', 'employee__first_name', 'employee__last_name', 'license_number']
	readonly_fields = ['availability_status']


@admin.register(VehicleMaintenance)
class VehicleMaintenanceAdmin(admin.ModelAdmin):
	list_display = ['vehicle', 'maintenance_type', 'service_date', 'cost', 'status', 'created_by']
	list_filter = ['maintenance_type', 'status', 'service_date']
	search_fields = ['vehicle__vehicle_number', 'service_provider']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
	list_display = ['route_number', 'origin_city', 'destination_city', 'distance_km', 'route_status', 'route_algorithm']
	list_filter = ['route_status', 'route_algorithm', 'origin_city', 'destination_city']
	search_fields = ['route_number', 'origin_city', 'destination_city']


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
	list_display = ['delivery_number', 'order', 'driver', 'vehicle', 'route', 'delivery_status']
	list_filter = ['delivery_status', 'driver', 'vehicle']
	search_fields = ['delivery_number', 'order__order_number', 'driver__employee__employee_code', 'vehicle__vehicle_number']
	readonly_fields = ['driver', 'vehicle', 'assigned_at', 'delivery_status', 'pickup_time', 'actual_delivery_time']


@admin.register(DeliveryStatusHistory)
class DeliveryStatusHistoryAdmin(admin.ModelAdmin):
	list_display = ['delivery', 'previous_status', 'new_status', 'changed_by', 'changed_at']
	list_filter = ['new_status', 'changed_at']
	search_fields = ['delivery__delivery_number', 'changed_by__email']
	readonly_fields = ['delivery', 'previous_status', 'new_status', 'changed_by', 'changed_at']
