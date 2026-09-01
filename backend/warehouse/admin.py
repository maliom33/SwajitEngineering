from django.contrib import admin

from .models import (
	Inventory,
	Product,
	ProductCategory,
	PurchaseOrder,
	PurchaseOrderItem,
	StockTransaction,
	StockTransfer,
	StockTransferItem,
	Supplier,
	Warehouse,
)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
	list_display = ['warehouse_code', 'warehouse_name', 'city', 'manager', 'status']
	list_filter = ['status', 'city']
	search_fields = ['warehouse_code', 'warehouse_name', 'city', 'manager__employee_code']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
	list_display = ['category_code', 'category_name', 'is_active', 'created_at']
	list_filter = ['is_active']
	search_fields = ['category_code', 'category_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['sku', 'product_code', 'product_name', 'category', 'unit_price', 'status']
	list_filter = ['status', 'category', 'unit']
	search_fields = ['sku', 'product_code', 'product_name']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
	list_display = ['supplier_code', 'supplier_name', 'contact_person', 'email', 'status']
	list_filter = ['status', 'city']
	search_fields = ['supplier_code', 'supplier_name', 'contact_person', 'email']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
	list_display = ['warehouse', 'product', 'quantity_available', 'quantity_reserved', 'quantity_damaged', 'reorder_level']
	list_filter = ['warehouse', 'product__category']
	search_fields = ['warehouse__warehouse_code', 'product__sku', 'product__product_name']
	readonly_fields = ['quantity_available', 'quantity_reserved', 'quantity_damaged', 'last_stock_update']


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
	list_display = ['warehouse', 'product', 'transaction_type', 'quantity', 'performed_by', 'transaction_date']
	list_filter = ['transaction_type', 'warehouse', 'transaction_date']
	search_fields = ['warehouse__warehouse_code', 'product__sku', 'reference_type', 'reference_id']
	readonly_fields = ['transaction_date', 'balance_after']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
	list_display = ['purchase_order_number', 'supplier', 'warehouse', 'order_date', 'total_amount', 'status', 'created_by']
	list_filter = ['status', 'warehouse', 'order_date']
	search_fields = ['purchase_order_number', 'supplier__supplier_code', 'supplier__supplier_name']


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
	list_display = ['purchase_order', 'product', 'quantity_ordered', 'quantity_received', 'unit_price', 'line_total']
	search_fields = ['purchase_order__purchase_order_number', 'product__sku']


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
	list_display = ['transfer_number', 'source_warehouse', 'destination_warehouse', 'transfer_date', 'status', 'initiated_by']
	list_filter = ['status', 'transfer_date']
	search_fields = ['transfer_number', 'source_warehouse__warehouse_code', 'destination_warehouse__warehouse_code']


@admin.register(StockTransferItem)
class StockTransferItemAdmin(admin.ModelAdmin):
	list_display = ['transfer', 'product', 'quantity', 'received_quantity']
	search_fields = ['transfer__transfer_number', 'product__sku']
