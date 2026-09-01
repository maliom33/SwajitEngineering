from rest_framework import serializers

from .models import Customer, CustomerCommunication, Order, OrderItem, OrderStatusHistory, Quotation, QuotationItem


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerCommunicationSerializer(serializers.ModelSerializer):
    handled_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CustomerCommunication
        fields = '__all__'


class QuotationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = '__all__'

    def validate(self, attrs):
        quantity = attrs.get('quantity', getattr(self.instance, 'quantity', None))
        unit_price = attrs.get('unit_price', getattr(self.instance, 'unit_price', None))
        tax_percentage = attrs.get('tax_percentage', getattr(self.instance, 'tax_percentage', 0))
        discount_amount = attrs.get('discount_amount', getattr(self.instance, 'discount_amount', 0))
        line_total = attrs.get('line_total', getattr(self.instance, 'line_total', None))
        expected = (quantity * unit_price) + (quantity * unit_price * tax_percentage / 100) - discount_amount
        if line_total != expected:
            raise serializers.ValidationError({'line_total': 'Line total does not match the item values.'})
        return attrs


class QuotationSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Quotation
        fields = '__all__'

    def validate(self, attrs):
        if attrs['valid_until'] < attrs['quotation_date']:
            raise serializers.ValidationError({'valid_until': 'Validity date cannot be before quotation date.'})
        expected = attrs['subtotal'] + attrs.get('tax_amount', 0) - attrs.get('discount_amount', 0)
        if attrs['total_amount'] != expected:
            raise serializers.ValidationError({'total_amount': 'Total must equal subtotal plus tax minus discount.'})
        return attrs


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def validate(self, attrs):
        quantity = attrs.get('quantity', getattr(self.instance, 'quantity', None))
        unit_price = attrs.get('unit_price', getattr(self.instance, 'unit_price', None))
        tax_percentage = attrs.get('tax_percentage', getattr(self.instance, 'tax_percentage', 0))
        discount_amount = attrs.get('discount_amount', getattr(self.instance, 'discount_amount', 0))
        line_total = attrs.get('line_total', getattr(self.instance, 'line_total', None))
        expected = (quantity * unit_price) + (quantity * unit_price * tax_percentage / 100) - discount_amount
        if line_total != expected:
            raise serializers.ValidationError({'line_total': 'Line total does not match the item values.'})
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    approved_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('expected_delivery_date') and attrs['expected_delivery_date'] < attrs['order_date']:
            raise serializers.ValidationError({'expected_delivery_date': 'Expected delivery cannot be before order date.'})
        expected = attrs['subtotal'] + attrs.get('tax_amount', 0) - attrs.get('discount_amount', 0)
        if attrs['total_amount'] != expected:
            raise serializers.ValidationError({'total_amount': 'Total must equal subtotal plus tax minus discount.'})
        return attrs


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderStatusHistory
        fields = '__all__'
        read_only_fields = ['history_id', 'previous_status', 'changed_by', 'changed_at']