from datetime import date, datetime, timedelta
from decimal import Decimal

from django.db.models import F, Avg, Count, Q, Sum
from django.utils import timezone

from dispatch.models import Dispatch
from finance.models import Expense, FinancialTransaction, Invoice, Payment
from logistics.models import Delivery, Driver, Vehicle
from recruitment.models import Candidate, Interview, JobApplication, JobPosition, RecruitmentScreening
from sales.models import Customer, Order
from warehouse.models import Inventory, Product, PurchaseOrder, StockTransaction, Warehouse
from workforce.models import Attendance, Employee, EmployeePerformance, PayrollItem


def parse_date_filters(params):
    start_raw = params.get('start_date')
    end_raw = params.get('end_date')
    try:
        start = date.fromisoformat(start_raw) if start_raw else None
        end = date.fromisoformat(end_raw) if end_raw else None
    except ValueError as error:
        raise ValueError('Dates must use YYYY-MM-DD format.') from error
    if start and end and start > end:
        raise ValueError('start_date cannot be after end_date.')
    return start, end


def _date_filter(queryset, field, start, end):
    if start:
        queryset = queryset.filter(**{f'{field}__gte': start})
    if end:
        queryset = queryset.filter(**{f'{field}__lte': end})
    return queryset


def _decimal(value):
    return value or Decimal('0')


def _percentage(numerator, denominator):
    if not denominator:
        return Decimal('0')
    return (Decimal(numerator) * Decimal('100') / Decimal(denominator)).quantize(Decimal('0.01'))


def workforce_analytics(start=None, end=None):
    employees = Employee.objects.all()
    attendance = _date_filter(Attendance.objects.all(), 'attendance_date', start, end)
    employee_total = employees.count()
    present = attendance.filter(status__in=['PRESENT', 'LATE', 'HALF_DAY']).count()
    attendance_total = attendance.count()
    return {
        'total_employees': employee_total,
        'active_employees': employees.filter(status=Employee.Status.ACTIVE).count(),
        'employees_on_leave': employees.filter(status=Employee.Status.ON_LEAVE).count(),
        'employees_by_department': list(employees.values('department__department_name').annotate(count=Count('employee_id')).order_by('department__department_name')),
        'employees_by_designation': list(employees.values('designation__designation_name').annotate(count=Count('employee_id')).order_by('designation__designation_name')),
        'employees_by_employment_type': list(employees.values('employment_type').annotate(count=Count('employee_id')).order_by('employment_type')),
        'attendance_percentage': _percentage(present, attendance_total),
        'present_employees': present,
        'absent_employees': attendance.filter(status='ABSENT').count(),
        'average_work_hours': _decimal(attendance.aggregate(value=Avg('work_hours'))['value']),
        'payroll_summary': {'gross_salary': _decimal(PayrollItem.objects.aggregate(value=Sum('gross_salary'))['value']), 'net_salary': _decimal(PayrollItem.objects.aggregate(value=Sum('net_salary'))['value'])},
        'performance_summary': {'average_score': _decimal(EmployeePerformance.objects.aggregate(value=Avg('overall_score'))['value']), 'reviews': EmployeePerformance.objects.count()},
    }


def recruitment_analytics(start=None, end=None):
    applications = _date_filter(JobApplication.objects.all(), 'application_date', start, end)
    candidates = _date_filter(Candidate.objects.all(), 'created_at', start, end)
    interviews = _date_filter(Interview.objects.all(), 'scheduled_at', start, end)
    shortlisted = applications.filter(application_status__in=['SHORTLISTED', 'INTERVIEW_SCHEDULED', 'INTERVIEWED', 'SELECTED']).count()
    interviewed = applications.filter(application_status__in=['INTERVIEWED', 'SELECTED']).count()
    selected = applications.filter(application_status='SELECTED').count()
    return {'open_jobs': JobPosition.objects.filter(status='OPEN').count(), 'applications': applications.count(), 'candidates': candidates.count(), 'candidates_by_status': list(candidates.values('candidate_status').annotate(count=Count('candidate_id'))), 'applications_by_job': list(applications.values('job__job_title').annotate(count=Count('application_id'))), 'shortlisted_candidates': shortlisted, 'rejected_candidates': applications.filter(application_status='REJECTED').count(), 'interviews': interviews.count(), 'selected_candidates': selected, 'average_screening_score': _decimal(RecruitmentScreening.objects.aggregate(value=Avg('overall_score'))['value']), 'conversion_rates': {'applications_to_shortlisted': _percentage(shortlisted, applications.count()), 'shortlisted_to_interviewed': _percentage(interviewed, shortlisted), 'interviewed_to_selected': _percentage(selected, interviewed)}}


def sales_analytics(start=None, end=None):
    orders = _date_filter(Order.objects.all(), 'order_date', start, end)
    revenue = _decimal(orders.exclude(order_status='CANCELLED').aggregate(value=Sum('total_amount'))['value'])
    return {'total_customers': Customer.objects.count(), 'total_orders': orders.count(), 'orders_by_status': list(orders.values('order_status').annotate(count=Count('order_id'))), 'sales_revenue': revenue, 'revenue_by_month': list(orders.exclude(order_status='CANCELLED').values('order_date__year', 'order_date__month').annotate(value=Sum('total_amount')).order_by('order_date__year', 'order_date__month')), 'revenue_by_customer': list(orders.exclude(order_status='CANCELLED').values('customer__company_name').annotate(value=Sum('total_amount')).order_by('-value')[:10]), 'top_products': list(orders.filter(items__product__isnull=False).values('items__product__product_name').annotate(quantity=Sum('items__quantity')).order_by('-quantity')[:10]), 'average_order_value': _decimal(orders.exclude(order_status='CANCELLED').aggregate(value=Avg('total_amount'))['value']), 'pending_orders': orders.filter(order_status__in=['DRAFT', 'PENDING_APPROVAL', 'CONFIRMED', 'PROCESSING', 'READY_FOR_DISPATCH']).count(), 'cancelled_orders': orders.filter(order_status='CANCELLED').count(), 'delivered_orders': orders.filter(order_status='DELIVERED').count()}


def warehouse_analytics(start=None, end=None):
    inventory = Inventory.objects.annotate(available_to_promise=F('quantity_available') - F('quantity_reserved'))
    return {'total_warehouses': Warehouse.objects.count(), 'active_warehouses': Warehouse.objects.filter(status='ACTIVE').count(), 'total_products': Product.objects.count(), 'total_inventory_quantity': _decimal(inventory.aggregate(value=Sum('quantity_available'))['value']), 'available_stock': _decimal(inventory.aggregate(value=Sum('quantity_available'))['value']) - _decimal(inventory.aggregate(value=Sum('quantity_reserved'))['value']), 'reserved_stock': _decimal(inventory.aggregate(value=Sum('quantity_reserved'))['value']), 'damaged_stock': _decimal(inventory.aggregate(value=Sum('quantity_damaged'))['value']), 'low_stock_products': inventory.filter(available_to_promise__lte=F('reorder_level')).count(), 'out_of_stock_products': inventory.filter(available_to_promise__lte=0).count(), 'inventory_by_warehouse': list(inventory.values('warehouse__warehouse_name').annotate(quantity=Sum('quantity_available'))), 'inventory_by_category': list(inventory.values('product__category__category_name').annotate(quantity=Sum('quantity_available'))), 'stock_transaction_summary': list(StockTransaction.objects.values('transaction_type').annotate(count=Count('transaction_id'), quantity=Sum('quantity'))), 'purchase_order_summary': list(PurchaseOrder.objects.values('status').annotate(count=Count('purchase_order_id'), total=Sum('total_amount')))}


def logistics_analytics(start=None, end=None):
    deliveries = _date_filter(Delivery.objects.all(), 'created_at', start, end)
    return {'total_deliveries': deliveries.count(), 'active_deliveries': deliveries.exclude(delivery_status__in=['DELIVERED', 'FAILED', 'CANCELLED']).count(), 'delivered_deliveries': deliveries.filter(delivery_status='DELIVERED').count(), 'failed_deliveries': deliveries.filter(delivery_status='FAILED').count(), 'cancelled_deliveries': deliveries.filter(delivery_status='CANCELLED').count(), 'in_transit_deliveries': deliveries.filter(delivery_status__in=['IN_TRANSIT', 'OUT_FOR_DELIVERY']).count(), 'deliveries_by_status': list(deliveries.values('delivery_status').annotate(count=Count('delivery_id'))), 'deliveries_by_driver': list(deliveries.filter(driver__isnull=False).values('driver__employee__first_name', 'driver__employee__last_name').annotate(count=Count('delivery_id'))), 'deliveries_by_vehicle': list(deliveries.filter(vehicle__isnull=False).values('vehicle__vehicle_number').annotate(count=Count('delivery_id'))), 'available_drivers': Driver.objects.filter(availability_status='AVAILABLE').count(), 'available_vehicles': Vehicle.objects.filter(status='AVAILABLE').count(), 'driver_utilization': _percentage(deliveries.filter(driver__isnull=False).exclude(delivery_status__in=['DELIVERED', 'FAILED', 'CANCELLED']).count(), deliveries.filter(driver__isnull=False).count()), 'vehicle_utilization': _percentage(deliveries.filter(vehicle__isnull=False).exclude(delivery_status__in=['DELIVERED', 'FAILED', 'CANCELLED']).count(), deliveries.filter(vehicle__isnull=False).count())}


def dispatch_analytics(start=None, end=None):
    dispatches = _date_filter(Dispatch.objects.all(), 'scheduled_dispatch_date', start, end)
    today = timezone.localdate()
    return {'today_dispatches': Dispatch.objects.filter(scheduled_dispatch_date=today).count(), 'scheduled_dispatches': dispatches.filter(dispatch_status='SCHEDULED').count(), 'preparing_dispatches': dispatches.filter(dispatch_status='PREPARING').count(), 'ready_dispatches': dispatches.filter(dispatch_status='READY').count(), 'handed_over_dispatches': dispatches.filter(dispatch_status='HANDED_OVER').count(), 'dispatched_shipments': dispatches.filter(dispatch_status='DISPATCHED').count(), 'cancelled_dispatches': dispatches.filter(dispatch_status='CANCELLED').count(), 'dispatches_by_warehouse': list(dispatches.values('warehouse__warehouse_name').annotate(count=Count('dispatch_id'))), 'dispatch_completion_rate': _percentage(dispatches.filter(dispatch_status='DISPATCHED').count(), dispatches.exclude(dispatch_status='CANCELLED').count())}


def finance_analytics(start=None, end=None):
    transactions = _date_filter(FinancialTransaction.objects.all(), 'transaction_date', start, end)
    payments = _date_filter(Payment.objects.filter(payment_status='SUCCESS'), 'payment_date', start, end)
    expenses = _date_filter(Expense.objects.filter(status__in=['APPROVED', 'PAID']), 'expense_date', start, end)
    invoices = Invoice.objects.all()
    revenue = _decimal(transactions.filter(transaction_type='PAYMENT_RECEIVED').aggregate(value=Sum('amount'))['value'])
    expense_total = _decimal(expenses.aggregate(value=Sum('amount'))['value'])
    return {'total_revenue': revenue, 'total_expenses': expense_total, 'total_payments_received': _decimal(payments.aggregate(value=Sum('amount'))['value']), 'outstanding_invoices': _decimal(invoices.filter(amount_due__gt=0).aggregate(value=Sum('amount_due'))['value']), 'overdue_invoices': _decimal(invoices.filter(status='OVERDUE').aggregate(value=Sum('amount_due'))['value']), 'net_financial_amount': revenue - expense_total, 'revenue_by_month': list(transactions.filter(transaction_type='PAYMENT_RECEIVED').values('transaction_date__year', 'transaction_date__month').annotate(value=Sum('amount'))), 'expenses_by_month': list(expenses.values('expense_date__year', 'expense_date__month').annotate(value=Sum('amount'))), 'payments_by_month': list(payments.values('payment_date__year', 'payment_date__month').annotate(value=Sum('amount'))), 'expenses_by_category': list(expenses.values('category__category_name').annotate(value=Sum('amount'))), 'payment_method_distribution': list(payments.values('payment_method').annotate(count=Count('payment_id'), amount=Sum('amount'))), 'invoice_status_distribution': list(invoices.values('status').annotate(count=Count('invoice_id')))}


def executive_dashboard():
    today = timezone.localdate()
    month_start = today.replace(day=1)
    workforce = workforce_analytics(today, today)
    sales = sales_analytics(month_start, today)
    recruitment = recruitment_analytics()
    warehouse = warehouse_analytics()
    logistics = logistics_analytics()
    dispatch = dispatch_analytics()
    finance = finance_analytics()
    return {'workforce': {'total_employees': workforce['total_employees'], 'active_employees': workforce['active_employees'], 'employees_on_leave': workforce['employees_on_leave'], 'todays_attendance': workforce['present_employees'], 'attendance_percentage': workforce['attendance_percentage']}, 'recruitment': {'open_job_positions': recruitment['open_jobs'], 'total_candidates': recruitment['candidates'], 'applications': recruitment['applications'], 'shortlisted_candidates': recruitment['shortlisted_candidates'], 'interviews_scheduled': recruitment['interviews'], 'selected_candidates': recruitment['selected_candidates']}, 'sales': {'total_customers': sales['total_customers'], 'orders_today': Order.objects.filter(order_date=today).count(), 'orders_this_month': Order.objects.filter(order_date__gte=month_start, order_date__lte=today).count(), 'sales_amount': sales['sales_revenue'], 'pending_orders': sales['pending_orders'], 'delivered_orders': sales['delivered_orders']}, 'warehouse': {'total_products': warehouse['total_products'], 'total_inventory_quantity': warehouse['total_inventory_quantity'], 'low_stock_products': warehouse['low_stock_products'], 'out_of_stock_products': warehouse['out_of_stock_products'], 'active_warehouses': warehouse['active_warehouses']}, 'logistics': {'active_deliveries': logistics['active_deliveries'], 'delivered_deliveries': logistics['delivered_deliveries'], 'in_transit_deliveries': logistics['in_transit_deliveries'], 'available_drivers': logistics['available_drivers'], 'available_vehicles': logistics['available_vehicles']}, 'dispatch': {'today_dispatches': dispatch['today_dispatches'], 'pending_dispatches': dispatch['scheduled_dispatches'] + dispatch['preparing_dispatches'], 'dispatched_shipments': dispatch['dispatched_shipments'], 'ready_for_dispatch': dispatch['ready_dispatches']}, 'finance': {'revenue': finance['total_revenue'], 'expenses': finance['total_expenses'], 'paid_amount': finance['total_payments_received'], 'outstanding_amount': finance['outstanding_invoices'], 'overdue_invoices': finance['overdue_invoices']}}


def kpis():
    sales = sales_analytics()
    logistics = logistics_analytics()
    finance = finance_analytics()
    return {'order_fulfillment_rate': _percentage(sales['delivered_orders'], sales['total_orders']), 'payment_collection_rate': _percentage(finance['total_payments_received'], finance['total_payments_received'] + finance['outstanding_invoices']), 'dispatch_completion_rate': _percentage(Dispatch.objects.filter(dispatch_status='DISPATCHED').count(), Dispatch.objects.exclude(dispatch_status='CANCELLED').count()), 'delivery_completion_rate': _percentage(logistics['delivered_deliveries'], logistics['total_deliveries'])}