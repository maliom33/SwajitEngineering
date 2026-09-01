from rest_framework import serializers

from .models import Delivery, DeliveryStatusHistory, Driver, Route, Vehicle, VehicleMaintenance


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['status']


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
        read_only_fields = ['availability_status']


class VehicleMaintenanceSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = VehicleMaintenance
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Route
        fields = '__all__'


class DeliverySerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    driver = serializers.PrimaryKeyRelatedField(read_only=True)
    vehicle = serializers.PrimaryKeyRelatedField(read_only=True)
    delivery_status = serializers.CharField(read_only=True)

    class Meta:
        model = Delivery
        fields = '__all__'


class DeliveryStatusHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DeliveryStatusHistory
        fields = '__all__'
        read_only_fields = fields