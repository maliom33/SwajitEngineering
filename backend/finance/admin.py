from django.contrib import admin

from .models import Expense, ExpenseCategory, FinancialTransaction, Invoice, InvoiceItem, Payment, Refund


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
	list_display = ['invoice_number', 'customer', 'order', 'invoice_date', 'due_date', 'total_amount', 'amount_due', 'status']
	list_filter = ['status', 'invoice_date', 'due_date']
	search_fields = ['invoice_number', 'customer__customer_code', 'order__order_number']
	readonly_fields = ['amount_paid', 'amount_due', 'status']


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
	list_display = ['invoice', 'product', 'description', 'quantity', 'unit_price', 'line_total']
	search_fields = ['invoice__invoice_number', 'product__sku', 'description']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ['payment_reference', 'invoice', 'amount', 'payment_method', 'payment_status', 'payment_date']
	list_filter = ['payment_method', 'payment_status', 'payment_date']
	search_fields = ['payment_reference', 'invoice__invoice_number', 'transaction_reference']
	readonly_fields = ['payment_status']


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
	list_display = ['category_code', 'category_name', 'is_active']
	list_filter = ['is_active']
	search_fields = ['category_code', 'category_name']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
	list_display = ['expense_number', 'category', 'amount', 'expense_date', 'status', 'recorded_by']
	list_filter = ['status', 'category', 'expense_date']
	search_fields = ['expense_number', 'category__category_code', 'vendor_name']
	readonly_fields = ['approved_by', 'status']


@admin.register(FinancialTransaction)
class FinancialTransactionAdmin(admin.ModelAdmin):
	list_display = ['transaction_number', 'transaction_type', 'amount', 'transaction_date', 'reference_type', 'created_by']
	list_filter = ['transaction_type', 'transaction_date']
	search_fields = ['transaction_number', 'reference_type', 'reference_id', 'description']
	readonly_fields = ['transaction_number', 'transaction_type', 'transaction_date', 'amount', 'reference_type', 'reference_id', 'created_by', 'created_at']


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
	list_display = ['refund_reference', 'payment', 'amount', 'refund_date', 'processed_by']
	list_filter = ['refund_date']
	search_fields = ['refund_reference', 'payment__payment_reference']
	readonly_fields = ['payment', 'amount', 'refund_date', 'processed_by', 'created_at']
