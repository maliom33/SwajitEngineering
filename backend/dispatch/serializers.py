from rest_framework import serializers

from .models import DeliveryChallan, Dispatch, DispatchDocument, DispatchItem, DispatchStatusHistory


class DispatchSerializer(serializers.ModelSerializer):
    prepared_by = serializers.PrimaryKeyRelatedField(read_only=True)
    handed_over_by = serializers.PrimaryKeyRelatedField(read_only=True)
    dispatch_status = serializers.CharField(read_only=True)

    class Meta:
        model = Dispatch
        fields = '__all__'


class DispatchItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchItem
        fields = '__all__'

    def validate(self, attrs):
        if attrs['quantity'] <= 0 or attrs['package_count'] < 1:
            raise serializers.ValidationError('Quantity must be positive and package count must be at least one.')
        return attrs


class DeliveryChallanSerializer(serializers.ModelSerializer):
    issued_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DeliveryChallan
        fields = '__all__'
        read_only_fields = ['vehicle_number_snapshot', 'driver_name_snapshot', 'delivery_address', 'total_items', 'total_quantity', 'status']


class DispatchStatusHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DispatchStatusHistory
        fields = '__all__'
        read_only_fields = fields


class DispatchDocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DispatchDocument
        fields = '__all__'
        read_only_fields = ['original_filename', 'uploaded_by', 'uploaded_at']

    def create(self, validated_data):
        uploaded = validated_data['file']
        validated_data['original_filename'] = uploaded.name
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)