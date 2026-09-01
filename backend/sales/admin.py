from django.contrib import admin

from .models import Customer, CustomerCommunication, Order, OrderItem, OrderStatusHistory, Quotation, QuotationItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ['customer_code', 'company_name', 'contact_person', 'email', 'phone', 'status', 'created_at']
	list_filter = ['customer_type', 'status', 'created_at']
	search_fields = ['customer_code', 'company_name', 'contact_person', 'email', 'phone']


@admin.register(CustomerCommunication)
class CustomerCommunicationAdmin(admin.ModelAdmin):
	list_display = ['customer', 'communication_type', 'subject', 'communication_date', 'handled_by', 'status']
	list_filter = ['communication_type', 'status', 'communication_date']
	search_fields = ['customer__customer_code', 'customer__company_name', 'subject']


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
	list_display = ['quotation_number', 'customer', 'quotation_date', 'valid_until', 'total_amount', 'status', 'created_by']
	list_filter = ['status', 'quotation_date', 'valid_until']
	search_fields = ['quotation_number', 'customer__customer_code', 'customer__company_name']


@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
	list_display = ['quotation', 'product', 'description', 'quantity', 'unit_price', 'line_total']
	search_fields = ['quotation__quotation_number', 'product__sku', 'description']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['order_number', 'customer', 'order_date', 'total_amount', 'priority', 'order_status', 'created_by']
	list_filter = ['order_status', 'priority', 'order_date']
	search_fields = ['order_number', 'customer__customer_code', 'customer__company_name']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ['order', 'product', 'description', 'quantity', 'unit_price', 'line_total']
	search_fields = ['order__order_number', 'product__sku', 'description']


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
	list_display = ['order', 'previous_status', 'new_status', 'changed_by', 'changed_at']
	list_filter = ['new_status', 'changed_at']
	search_fields = ['order__order_number', 'changed_by__email']
