from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from accounts.permissions import HasPermission

from .models import Delivery, DeliveryStatusHistory, Driver, Route, Vehicle, VehicleMaintenance
from .serializers import DeliverySerializer, DeliveryStatusHistorySerializer, DriverSerializer, RouteSerializer, VehicleMaintenanceSerializer, VehicleSerializer
from .services.delivery_service import assign_delivery, create_delivery, update_delivery_status


class LogisticsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    write_permissions = {}

    def get_permissions(self):
        permissions = [IsAuthenticated]
        required = self.write_permissions.get(self.action)
        if required:
            self.required_permission = required
            permissions.append(HasPermission)
        return [permission() for permission in permissions]


class VehicleViewSet(LogisticsViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    write_permissions = {'create': 'MANAGE_VEHICLES', 'update': 'MANAGE_VEHICLES', 'partial_update': 'MANAGE_VEHICLES', 'destroy': 'MANAGE_VEHICLES'}

    @action(detail=False, methods=['get'])
    def available(self, request):
        return Response(self.get_serializer(self.get_queryset().filter(status=Vehicle.Status.AVAILABLE), many=True).data)


class DriverViewSet(LogisticsViewSet):
    queryset = Driver.objects.select_related('employee').all()
    serializer_class = DriverSerializer
    write_permissions = {'create': 'MANAGE_DRIVERS', 'update': 'MANAGE_DRIVERS', 'partial_update': 'MANAGE_DRIVERS', 'destroy': 'MANAGE_DRIVERS'}

    @action(detail=False, methods=['get'])
    def available(self, request):
        return Response(self.get_serializer(self.get_queryset().filter(availability_status=Driver.AvailabilityStatus.AVAILABLE), many=True).data)


class VehicleMaintenanceViewSet(LogisticsViewSet):
    queryset = VehicleMaintenance.objects.select_related('vehicle', 'created_by').all()
    serializer_class = VehicleMaintenanceSerializer
    write_permissions = {'create': 'MANAGE_VEHICLE_MAINTENANCE', 'update': 'MANAGE_VEHICLE_MAINTENANCE', 'partial_update': 'MANAGE_VEHICLE_MAINTENANCE', 'destroy': 'MANAGE_VEHICLE_MAINTENANCE'}

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RouteViewSet(LogisticsViewSet):
    queryset = Route.objects.select_related('created_by').all()
    serializer_class = RouteSerializer
    write_permissions = {'create': 'MANAGE_ROUTES', 'update': 'MANAGE_ROUTES', 'partial_update': 'MANAGE_ROUTES', 'destroy': 'MANAGE_ROUTES'}

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DeliveryViewSet(LogisticsViewSet):
    queryset = Delivery.objects.select_related('order', 'driver', 'vehicle', 'route', 'created_by').all()
    serializer_class = DeliverySerializer
    write_permissions = {'create': 'MANAGE_DELIVERIES', 'update': 'MANAGE_DELIVERIES', 'partial_update': 'MANAGE_DELIVERIES', 'destroy': 'MANAGE_DELIVERIES', 'assign': 'ASSIGN_DELIVERIES', 'change_status': 'UPDATE_DELIVERY_STATUS'}

    def perform_create(self, serializer):
        order = serializer.validated_data['order']
        delivery = create_delivery(order=order, created_by=self.request.user, delivery_number=serializer.validated_data['delivery_number'], route=serializer.validated_data.get('route'), expected_delivery_time=serializer.validated_data.get('expected_delivery_time'), delivery_notes=serializer.validated_data.get('delivery_notes', ''))
        serializer.instance = delivery

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        delivery = self.get_object()
        try:
            result = assign_delivery(delivery, driver=Driver.objects.get(pk=request.data.get('driver')), vehicle=Vehicle.objects.get(pk=request.data.get('vehicle')), changed_by=request.user)
        except (Driver.DoesNotExist, Vehicle.DoesNotExist, ValueError) as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(result).data)

    @action(detail=True, methods=['post'], url_path='status')
    def change_status(self, request, pk=None):
        try:
            result = update_delivery_status(self.get_object(), new_status=request.data.get('new_status'), changed_by=request.user, location_description=request.data.get('location_description', ''), remarks=request.data.get('remarks', ''))
        except ValueError as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(result).data)

    @action(detail=True, methods=['get'], url_path='status-history')
    def status_history(self, request, pk=None):
        return Response(DeliveryStatusHistorySerializer(self.get_object().status_history.all(), many=True).data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        active = Delivery.objects.exclude(delivery_status__in=[Delivery.Status.DELIVERED, Delivery.Status.FAILED, Delivery.Status.CANCELLED])
        return Response(self.get_serializer(active, many=True).data)


class DeliveryStatusHistoryViewSet(ReadOnlyModelViewSet):
    queryset = DeliveryStatusHistory.objects.select_related('delivery', 'changed_by').all()
    serializer_class = DeliveryStatusHistorySerializer
    permission_classes = [IsAuthenticated]
