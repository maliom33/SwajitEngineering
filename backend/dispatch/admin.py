from django.contrib import admin

from .models import DeliveryChallan, Dispatch, DispatchDocument, DispatchItem, DispatchStatusHistory


@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
	list_display = ['dispatch_number', 'order', 'delivery', 'warehouse', 'scheduled_dispatch_date', 'dispatch_status']
	list_filter = ['dispatch_status', 'warehouse', 'scheduled_dispatch_date']
	search_fields = ['dispatch_number', 'order__order_number', 'delivery__delivery_number']
	readonly_fields = ['dispatch_status', 'actual_dispatch_date', 'handed_over_by']


@admin.register(DispatchItem)
class DispatchItemAdmin(admin.ModelAdmin):
	list_display = ['dispatch', 'product', 'quantity', 'package_count', 'created_at']
	search_fields = ['dispatch__dispatch_number', 'product__sku', 'product__product_name']


@admin.register(DeliveryChallan)
class DeliveryChallanAdmin(admin.ModelAdmin):
	list_display = ['challan_number', 'dispatch', 'challan_date', 'status', 'vehicle_number_snapshot', 'driver_name_snapshot']
	list_filter = ['status', 'challan_date']
	search_fields = ['challan_number', 'dispatch__dispatch_number', 'vehicle_number_snapshot', 'driver_name_snapshot']


@admin.register(DispatchStatusHistory)
class DispatchStatusHistoryAdmin(admin.ModelAdmin):
	list_display = ['dispatch', 'previous_status', 'new_status', 'changed_by', 'changed_at']
	list_filter = ['new_status', 'changed_at']
	search_fields = ['dispatch__dispatch_number', 'changed_by__email']
	readonly_fields = ['dispatch', 'previous_status', 'new_status', 'changed_by', 'changed_at']


@admin.register(DispatchDocument)
class DispatchDocumentAdmin(admin.ModelAdmin):
	list_display = ['dispatch', 'document_type', 'original_filename', 'uploaded_by', 'uploaded_at']
	list_filter = ['document_type', 'uploaded_at']
	search_fields = ['dispatch__dispatch_number', 'original_filename']
