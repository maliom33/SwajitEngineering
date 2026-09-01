from rest_framework import serializers

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


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    available_quantity = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'
        read_only_fields = ['quantity_available', 'quantity_reserved', 'quantity_damaged', 'last_stock_update']


class StockTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransaction
        fields = '__all__'
        read_only_fields = fields


class PurchaseOrderSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    approved_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('expected_delivery_date') and attrs['expected_delivery_date'] < attrs['order_date']:
            raise serializers.ValidationError({'expected_delivery_date': 'Expected delivery cannot be before order date.'})
        expected = attrs['subtotal'] + attrs.get('tax_amount', 0) - attrs.get('discount_amount', 0)
        if attrs['total_amount'] != expected:
            raise serializers.ValidationError({'total_amount': 'Total must equal subtotal plus tax minus discount.'})
        return attrs


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('quantity_received', 0) > attrs['quantity_ordered']:
            raise serializers.ValidationError({'quantity_received': 'Received quantity cannot exceed ordered quantity.'})
        return attrs


class StockTransferSerializer(serializers.ModelSerializer):
    initiated_by = serializers.PrimaryKeyRelatedField(read_only=True)
    approved_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StockTransfer
        fields = '__all__'

    def validate(self, attrs):
        if attrs['source_warehouse'] == attrs['destination_warehouse']:
            raise serializers.ValidationError({'destination_warehouse': 'Source and destination must differ.'})
        return attrs


class StockTransferItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransferItem
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('received_quantity', 0) > attrs['quantity']:
            raise serializers.ValidationError({'received_quantity': 'Received quantity cannot exceed transfer quantity.'})
        return attrs