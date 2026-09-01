from datetime import date

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from accounts.permissions import HasPermission

from .models import DeliveryChallan, Dispatch, DispatchDocument, DispatchItem, DispatchStatusHistory
from .serializers import DeliveryChallanSerializer, DispatchDocumentSerializer, DispatchItemSerializer, DispatchSerializer, DispatchStatusHistorySerializer
from .services.dispatch_service import cancel_dispatch, confirm_dispatch, create_dispatch, generate_delivery_challan, handover_dispatch, prepare_dispatch


class DispatchViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    write_permissions = {}

    def get_permissions(self):
        permissions = [IsAuthenticated]
        required = self.write_permissions.get(self.action)
        if required:
            self.required_permission = required
            permissions.append(HasPermission)
        return [permission() for permission in permissions]


class DispatchRecordViewSet(DispatchViewSet):
    queryset = Dispatch.objects.select_related('order', 'delivery', 'warehouse', 'prepared_by', 'handed_over_by').prefetch_related('items').all()
    serializer_class = DispatchSerializer
    write_permissions = {'create': 'CREATE_DISPATCH', 'update': 'MANAGE_DISPATCH', 'partial_update': 'MANAGE_DISPATCH', 'destroy': 'MANAGE_DISPATCH', 'prepare': 'PREPARE_DISPATCH', 'generate_challan': 'GENERATE_DELIVERY_CHALLAN', 'handover': 'HANDOVER_DISPATCH', 'confirm': 'UPDATE_DISPATCH_STATUS', 'cancel': 'UPDATE_DISPATCH_STATUS'}

    def perform_create(self, serializer):
        dispatch = create_dispatch(order=serializer.validated_data['order'], delivery=serializer.validated_data['delivery'], warehouse=serializer.validated_data['warehouse'], dispatch_number=serializer.validated_data['dispatch_number'], prepared_by=self.request.user, scheduled_dispatch_date=serializer.validated_data['scheduled_dispatch_date'], remarks=serializer.validated_data.get('remarks', ''))
        serializer.instance = dispatch

    @action(detail=True, methods=['post'])
    def prepare(self, request, pk=None):
        try:
            result = prepare_dispatch(self.get_object(), items=request.data.get('items', []), changed_by=request.user)
        except (ValueError, KeyError, TypeError) as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(result).data)

    @action(detail=True, methods=['post'], url_path='generate-challan')
    def generate_challan(self, request, pk=None):
        try:
            challan = generate_delivery_challan(self.get_object(), issued_by=request.user, challan_number=request.data.get('challan_number'))
        except ValueError as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(DeliveryChallanSerializer(challan).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def handover(self, request, pk=None):
        try:
            result = handover_dispatch(self.get_object(), handed_over_by=request.user)
        except ValueError as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(result).data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        try:
            result = confirm_dispatch(self.get_object(), confirmed_by=request.user)
        except ValueError as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(result).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        try:
            result = cancel_dispatch(self.get_object(), cancelled_by=request.user, remarks=request.data.get('remarks', ''))
        except ValueError as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(result).data)

    @action(detail=False, methods=['get'], url_path='ready-for-dispatch')
    def ready_for_dispatch(self, request):
        return Response(self.get_serializer(self.get_queryset().filter(dispatch_status=Dispatch.Status.READY), many=True).data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        return Response(self.get_serializer(self.get_queryset().filter(scheduled_dispatch_date=date.today()), many=True).data)

    @action(detail=False, methods=['get'])
    def history(self, request):
        return Response(DispatchStatusHistorySerializer(DispatchStatusHistory.objects.select_related('dispatch', 'changed_by').all(), many=True).data)


class DispatchItemViewSet(DispatchViewSet):
    queryset = DispatchItem.objects.select_related('dispatch', 'product').all()
    serializer_class = DispatchItemSerializer
    write_permissions = {'create': 'PREPARE_DISPATCH', 'update': 'PREPARE_DISPATCH', 'partial_update': 'PREPARE_DISPATCH', 'destroy': 'PREPARE_DISPATCH'}


class DeliveryChallanViewSet(DispatchViewSet):
    queryset = DeliveryChallan.objects.select_related('dispatch', 'issued_by').all()
    serializer_class = DeliveryChallanSerializer
    write_permissions = {'update': 'MANAGE_DISPATCH', 'partial_update': 'MANAGE_DISPATCH', 'destroy': 'MANAGE_DISPATCH'}


class DispatchStatusHistoryViewSet(ReadOnlyModelViewSet):
    queryset = DispatchStatusHistory.objects.select_related('dispatch', 'changed_by').all()
    serializer_class = DispatchStatusHistorySerializer
    permission_classes = [IsAuthenticated]


class DispatchDocumentViewSet(DispatchViewSet):
    queryset = DispatchDocument.objects.select_related('dispatch', 'uploaded_by').all()
    serializer_class = DispatchDocumentSerializer
    write_permissions = {'create': 'MANAGE_DISPATCH', 'update': 'MANAGE_DISPATCH', 'partial_update': 'MANAGE_DISPATCH', 'destroy': 'MANAGE_DISPATCH'}
