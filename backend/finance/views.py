from datetime import date

from django.db.models import Count, Q, Sum
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from accounts.permissions import HasPermission
from sales.models import Order

from .models import Expense, ExpenseCategory, FinancialTransaction, Invoice, InvoiceItem, Payment
from .serializers import ExpenseCategorySerializer, ExpenseSerializer, FinancialTransactionSerializer, InvoiceItemSerializer, InvoiceSerializer, PaymentSerializer
from .services.finance_service import approve_expense, create_invoice_from_order, record_payment, refund_payment, reject_expense, update_invoice_statuses


class FinanceViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    write_permissions = {}

    def get_permissions(self):
        permissions = [IsAuthenticated]
        required = self.write_permissions.get(self.action)
        if required:
            self.required_permission = required
            permissions.append(HasPermission)
        return [permission() for permission in permissions]


class InvoiceViewSet(FinanceViewSet):
    queryset = Invoice.objects.select_related('order', 'customer', 'created_by').prefetch_related('items', 'payments').all()
    serializer_class = InvoiceSerializer
    write_permissions = {'create': 'CREATE_INVOICE', 'update': 'MANAGE_INVOICES', 'partial_update': 'MANAGE_INVOICES', 'destroy': 'MANAGE_INVOICES', 'record_payment_action': 'RECORD_PAYMENT', 'cancel': 'MANAGE_INVOICES'}

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        update_invoice_statuses()
        return Response(self.get_serializer(self.get_queryset().filter(status=Invoice.Status.OVERDUE), many=True).data)

    @action(detail=True, methods=['post'], url_path='record-payment')
    def record_payment_action(self, request, pk=None):
        try:
            payment = record_payment(invoice=self.get_object(), payment_reference=request.data['payment_reference'], amount=request.data['amount'], payment_date=request.data.get('payment_date', date.today()), payment_method=request.data['payment_method'], received_by=request.user, transaction_reference=request.data.get('transaction_reference', ''), notes=request.data.get('notes', ''))
        except (KeyError, ValueError) as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        invoice = self.get_object()
        if invoice.status in [Invoice.Status.PAID, Invoice.Status.CANCELLED, Invoice.Status.VOID]:
            return Response({'detail': 'This invoice cannot be cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
        invoice.status = Invoice.Status.CANCELLED
        invoice.save(update_fields=['status', 'updated_at'])
        return Response(self.get_serializer(invoice).data)


class InvoiceItemViewSet(FinanceViewSet):
    queryset = InvoiceItem.objects.select_related('invoice', 'product').all()
    serializer_class = InvoiceItemSerializer
    write_permissions = {'create': 'MANAGE_INVOICES', 'update': 'MANAGE_INVOICES', 'partial_update': 'MANAGE_INVOICES', 'destroy': 'MANAGE_INVOICES'}


class PaymentViewSet(FinanceViewSet):
    queryset = Payment.objects.select_related('invoice', 'received_by').all()
    serializer_class = PaymentSerializer
    write_permissions = {'create': 'MANAGE_PAYMENTS', 'update': 'MANAGE_PAYMENTS', 'partial_update': 'MANAGE_PAYMENTS', 'destroy': 'MANAGE_PAYMENTS', 'refund': 'MANAGE_PAYMENTS'}

    def create(self, request, *args, **kwargs):
        return Response({'detail': 'Use the invoice record-payment endpoint.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Payments are immutable; use refund.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    partial_update = update

    def destroy(self, request, *args, **kwargs):
        return Response({'detail': 'Payments are immutable; use refund.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        try:
            result = refund_payment(payment=self.get_object(), amount=request.data['amount'], processed_by=request.user, refund_reference=request.data['refund_reference'], notes=request.data.get('notes', ''))
        except (KeyError, ValueError) as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'refund_id': result.pk, 'refund_reference': result.refund_reference}, status=status.HTTP_201_CREATED)


class ExpenseCategoryViewSet(FinanceViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    write_permissions = {'create': 'MANAGE_EXPENSES', 'update': 'MANAGE_EXPENSES', 'partial_update': 'MANAGE_EXPENSES', 'destroy': 'MANAGE_EXPENSES'}


class ExpenseViewSet(FinanceViewSet):
    queryset = Expense.objects.select_related('category', 'recorded_by', 'approved_by').all()
    serializer_class = ExpenseSerializer
    write_permissions = {'create': 'MANAGE_EXPENSES', 'update': 'MANAGE_EXPENSES', 'partial_update': 'MANAGE_EXPENSES', 'destroy': 'MANAGE_EXPENSES', 'approve': 'APPROVE_EXPENSES', 'reject': 'APPROVE_EXPENSES'}

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        try:
            expense = approve_expense(expense=self.get_object(), approved_by=request.user)
        except ValueError as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(expense).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        try:
            expense = reject_expense(expense=self.get_object(), approved_by=request.user)
        except ValueError as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(expense).data)


class FinancialTransactionViewSet(ReadOnlyModelViewSet):
    queryset = FinancialTransaction.objects.select_related('created_by').all()
    serializer_class = FinancialTransactionSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = 'VIEW_FINANCIAL_TRANSACTIONS'


class FinanceDashboardViewSet(FinanceViewSet):
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        update_invoice_statuses()
        revenue = FinancialTransaction.objects.filter(transaction_type=FinancialTransaction.Type.PAYMENT_RECEIVED).aggregate(total=Sum('amount'))['total'] or 0
        expenses = FinancialTransaction.objects.filter(transaction_type=FinancialTransaction.Type.EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
        paid = Payment.objects.filter(payment_status=Payment.Status.SUCCESS).aggregate(total=Sum('amount'))['total'] or 0
        outstanding = Invoice.objects.filter(amount_due__gt=0).aggregate(total=Sum('amount_due'))['total'] or 0
        overdue = Invoice.objects.filter(status=Invoice.Status.OVERDUE).aggregate(total=Sum('amount_due'))['total'] or 0
        return Response({'total_revenue': revenue, 'total_expenses': expenses, 'total_paid': paid, 'total_outstanding': outstanding, 'overdue_amount': overdue, 'pending_invoices': Invoice.objects.filter(status__in=[Invoice.Status.ISSUED, Invoice.Status.PARTIALLY_PAID]).count(), 'overdue_invoices': Invoice.objects.filter(status=Invoice.Status.OVERDUE).count(), 'recent_payments': PaymentSerializer(Payment.objects.order_by('-payment_date')[:5], many=True).data, 'recent_expenses': ExpenseSerializer(Expense.objects.order_by('-expense_date')[:5], many=True).data, 'recent_transactions': FinancialTransactionSerializer(FinancialTransaction.objects.order_by('-transaction_date')[:10], many=True).data})


class CreateInvoiceView(FinanceViewSet):
    @action(detail=True, methods=['post'])
    def create_invoice(self, request, pk=None):
        order = Order.objects.get(pk=pk)
        try:
            invoice = create_invoice_from_order(order=order, created_by=request.user, invoice_number=request.data['invoice_number'], due_date=request.data['due_date'], invoice_date=request.data.get('invoice_date'), currency=request.data.get('currency', 'INR'), notes=request.data.get('notes', ''))
        except (Order.DoesNotExist, KeyError, ValueError) as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(InvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)
