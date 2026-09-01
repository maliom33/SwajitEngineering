from rest_framework import serializers

from .models import Expense, ExpenseCategory, FinancialTransaction, Invoice, InvoiceItem, Payment


class InvoiceSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    amount_paid = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    amount_due = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    received_by = serializers.PrimaryKeyRelatedField(read_only=True)
    payment_status = serializers.CharField(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    recorded_by = serializers.PrimaryKeyRelatedField(read_only=True)
    approved_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['status', 'approved_by']


class FinancialTransactionSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FinancialTransaction
        fields = '__all__'
        read_only_fields = fields