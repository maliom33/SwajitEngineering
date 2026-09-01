from decimal import Decimal
from uuid import uuid4

from django.db import transaction
from django.utils import timezone

from ..models import Expense, FinancialTransaction, Invoice, InvoiceItem, Payment, Refund


def _transaction_number(prefix):
    return f'{prefix}-{uuid4().hex[:12].upper()}'


def _invoice_status(invoice):
    if invoice.amount_due <= 0:
        return Invoice.Status.PAID
    if invoice.due_date < timezone.localdate():
        return Invoice.Status.OVERDUE
    if invoice.amount_paid > 0:
        return Invoice.Status.PARTIALLY_PAID
    return Invoice.Status.ISSUED


@transaction.atomic
def create_invoice_from_order(*, order, created_by, invoice_number, due_date, invoice_date=None, currency='INR', notes=''):
    if hasattr(order, 'invoice'):
        raise ValueError('This sales order already has an invoice.')
    invoice_date = invoice_date or timezone.localdate()
    invoice = Invoice.objects.create(invoice_number=invoice_number, order=order, customer=order.customer, invoice_date=invoice_date, due_date=due_date, subtotal=0, tax_amount=0, discount_amount=0, total_amount=0, amount_due=0, currency=currency, status=Invoice.Status.DRAFT, created_by=created_by, notes=notes)
    subtotal = Decimal('0')
    tax_amount = Decimal('0')
    discount_amount = Decimal('0')
    for order_item in order.items.all():
        line_subtotal = order_item.quantity * order_item.unit_price
        line_tax = line_subtotal * order_item.tax_percentage / 100
        line_total = line_subtotal + line_tax - order_item.discount_amount
        InvoiceItem.objects.create(invoice=invoice, product=order_item.product, description=order_item.description, quantity=order_item.quantity, unit_price=order_item.unit_price, tax_percentage=order_item.tax_percentage, discount_amount=order_item.discount_amount, line_total=line_total)
        subtotal += line_subtotal
        tax_amount += line_tax
        discount_amount += order_item.discount_amount
    invoice.subtotal = subtotal
    invoice.tax_amount = tax_amount
    invoice.discount_amount = discount_amount
    invoice.total_amount = subtotal + tax_amount - discount_amount
    invoice.amount_due = invoice.total_amount
    invoice.status = Invoice.Status.ISSUED
    invoice.save(update_fields=['subtotal', 'tax_amount', 'discount_amount', 'total_amount', 'amount_due', 'status', 'updated_at'])
    return invoice


@transaction.atomic
def record_payment(*, invoice, payment_reference, amount, payment_date, payment_method, received_by, transaction_reference='', notes=''):
    invoice = Invoice.objects.select_for_update().get(pk=invoice.pk)
    amount = Decimal(str(amount))
    if invoice.status in [Invoice.Status.CANCELLED, Invoice.Status.VOID, Invoice.Status.PAID]:
        raise ValueError('This invoice cannot accept a payment.')
    if amount <= 0 or amount > invoice.amount_due:
        raise ValueError('Payment must be positive and cannot exceed the outstanding amount.')
    payment = Payment.objects.create(payment_reference=payment_reference, invoice=invoice, payment_date=payment_date, amount=amount, payment_method=payment_method, payment_status=Payment.Status.SUCCESS, transaction_reference=transaction_reference, received_by=received_by, notes=notes)
    invoice.amount_paid += amount
    invoice.amount_due = invoice.total_amount - invoice.amount_paid
    invoice.status = _invoice_status(invoice)
    invoice.save(update_fields=['amount_paid', 'amount_due', 'status', 'updated_at'])
    FinancialTransaction.objects.create(transaction_number=_transaction_number('TXN'), transaction_type=FinancialTransaction.Type.PAYMENT_RECEIVED, amount=amount, reference_type='Payment', reference_id=payment.pk, description=f'Payment received for {invoice.invoice_number}', created_by=received_by)
    return payment


@transaction.atomic
def approve_expense(*, expense, approved_by):
    expense = Expense.objects.select_for_update().get(pk=expense.pk)
    if expense.status != Expense.Status.PENDING_APPROVAL:
        raise ValueError('Only pending expenses can be approved.')
    expense.status = Expense.Status.APPROVED
    expense.approved_by = approved_by
    expense.save(update_fields=['status', 'approved_by', 'updated_at'])
    FinancialTransaction.objects.create(transaction_number=_transaction_number('TXN'), transaction_type=FinancialTransaction.Type.EXPENSE, amount=expense.amount, reference_type='Expense', reference_id=expense.pk, description=expense.description, created_by=approved_by)
    return expense


@transaction.atomic
def reject_expense(*, expense, approved_by):
    expense = Expense.objects.select_for_update().get(pk=expense.pk)
    if expense.status != Expense.Status.PENDING_APPROVAL:
        raise ValueError('Only pending expenses can be rejected.')
    expense.status = Expense.Status.REJECTED
    expense.approved_by = approved_by
    expense.save(update_fields=['status', 'approved_by', 'updated_at'])
    return expense


@transaction.atomic
def refund_payment(*, payment, amount, processed_by, refund_reference, notes=''):
    payment = Payment.objects.select_for_update().get(pk=payment.pk)
    amount = Decimal(str(amount))
    already_refunded = sum((refund.amount for refund in payment.refunds.all()), Decimal('0'))
    if payment.payment_status != Payment.Status.SUCCESS or amount <= 0 or already_refunded + amount > payment.amount:
        raise ValueError('Refund amount is invalid for this payment.')
    refund = Refund.objects.create(payment=payment, refund_reference=refund_reference, amount=amount, refund_date=timezone.localdate(), processed_by=processed_by, notes=notes)
    invoice = Invoice.objects.select_for_update().get(pk=payment.invoice_id)
    invoice.amount_paid -= amount
    invoice.amount_due = invoice.total_amount - invoice.amount_paid
    invoice.status = _invoice_status(invoice)
    invoice.save(update_fields=['amount_paid', 'amount_due', 'status', 'updated_at'])
    if already_refunded + amount == payment.amount:
        payment.payment_status = Payment.Status.REFUNDED
        payment.save(update_fields=['payment_status', 'updated_at'])
    FinancialTransaction.objects.create(transaction_number=_transaction_number('TXN'), transaction_type=FinancialTransaction.Type.REFUND, amount=amount, reference_type='Refund', reference_id=refund.pk, description=f'Refund for {payment.payment_reference}', created_by=processed_by)
    return refund


@transaction.atomic
def update_invoice_statuses():
    invoices = Invoice.objects.filter(amount_due__gt=0, due_date__lt=timezone.localdate()).exclude(status__in=[Invoice.Status.CANCELLED, Invoice.Status.VOID, Invoice.Status.OVERDUE])
    return invoices.update(status=Invoice.Status.OVERDUE)