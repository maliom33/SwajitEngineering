from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from accounts.permissions import HasPermission

from .models import Customer, CustomerCommunication, Order, OrderItem, OrderStatusHistory, Quotation, QuotationItem
from .serializers import (
    CustomerCommunicationSerializer,
    CustomerSerializer,
    OrderItemSerializer,
    OrderSerializer,
    OrderStatusHistorySerializer,
    QuotationItemSerializer,
    QuotationSerializer,
)


class SalesViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    write_permissions = {}

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        required_permission = self.write_permissions.get(self.action)
        if required_permission:
            self.required_permission = required_permission
            permission_classes.append(HasPermission)
        return [permission() for permission in permission_classes]


class CustomerViewSet(SalesViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    write_permissions = {'create': 'MANAGE_CUSTOMERS', 'update': 'MANAGE_CUSTOMERS', 'partial_update': 'MANAGE_CUSTOMERS', 'destroy': 'MANAGE_CUSTOMERS'}


class CustomerCommunicationViewSet(SalesViewSet):
    queryset = CustomerCommunication.objects.select_related('customer', 'handled_by').all()
    serializer_class = CustomerCommunicationSerializer
    write_permissions = {'create': 'MANAGE_CUSTOMER_COMMUNICATION', 'update': 'MANAGE_CUSTOMER_COMMUNICATION', 'partial_update': 'MANAGE_CUSTOMER_COMMUNICATION', 'destroy': 'MANAGE_CUSTOMER_COMMUNICATION'}

    def perform_create(self, serializer):
        serializer.save(handled_by=self.request.user)


class QuotationViewSet(SalesViewSet):
    queryset = Quotation.objects.select_related('customer', 'created_by').prefetch_related('items').all()
    serializer_class = QuotationSerializer
    write_permissions = {'create': 'MANAGE_QUOTATIONS', 'update': 'MANAGE_QUOTATIONS', 'partial_update': 'MANAGE_QUOTATIONS', 'destroy': 'MANAGE_QUOTATIONS', 'items': 'MANAGE_QUOTATIONS'}

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get', 'post'], url_path='items')
    def items(self, request, pk=None):
        quotation = self.get_object()
        if request.method == 'GET':
            return Response(QuotationItemSerializer(quotation.items.all(), many=True).data)
        self.required_permission = 'MANAGE_QUOTATIONS'
        if not request.user.role or not request.user.role.role_permissions.filter(permission__permission_code=self.required_permission).exists():
            return Response({'detail': 'You do not have the required permission.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = QuotationItemSerializer(data={**request.data, 'quotation': quotation.pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuotationItemViewSet(SalesViewSet):
    queryset = QuotationItem.objects.select_related('quotation').all()
    serializer_class = QuotationItemSerializer
    write_permissions = {'create': 'MANAGE_QUOTATIONS', 'update': 'MANAGE_QUOTATIONS', 'partial_update': 'MANAGE_QUOTATIONS', 'destroy': 'MANAGE_QUOTATIONS'}


class OrderViewSet(SalesViewSet):
    queryset = Order.objects.select_related('customer', 'quotation', 'created_by', 'approved_by').prefetch_related('items', 'status_history').all()
    serializer_class = OrderSerializer
    write_permissions = {'create': 'CREATE_SALES_ORDER', 'update': 'UPDATE_SALES_ORDER', 'partial_update': 'UPDATE_SALES_ORDER', 'destroy': 'UPDATE_SALES_ORDER', 'change_status': 'MANAGE_ORDER_STATUS', 'items': 'CREATE_SALES_ORDER'}

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get', 'post'], url_path='items')
    def items(self, request, pk=None):
        order = self.get_object()
        if request.method == 'GET':
            return Response(OrderItemSerializer(order.items.all(), many=True).data)
        if not request.user.role or not request.user.role.role_permissions.filter(permission__permission_code='CREATE_SALES_ORDER').exists():
            return Response({'detail': 'You do not have the required permission.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderItemSerializer(data={**request.data, 'order': order.pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='status-history')
    def status_history(self, request, pk=None):
        return Response(OrderStatusHistorySerializer(self.get_object().status_history.all(), many=True).data)

    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('new_status')
        remarks = request.data.get('remarks', '')
        valid_transitions = {
            Order.Status.DRAFT: {Order.Status.PENDING_APPROVAL, Order.Status.CANCELLED},
            Order.Status.PENDING_APPROVAL: {Order.Status.CONFIRMED, Order.Status.ON_HOLD, Order.Status.CANCELLED},
            Order.Status.CONFIRMED: {Order.Status.PROCESSING, Order.Status.ON_HOLD, Order.Status.CANCELLED},
            Order.Status.PROCESSING: {Order.Status.READY_FOR_DISPATCH, Order.Status.ON_HOLD},
            Order.Status.READY_FOR_DISPATCH: {Order.Status.DISPATCHED},
            Order.Status.DISPATCHED: {Order.Status.DELIVERED},
            Order.Status.ON_HOLD: {Order.Status.CONFIRMED, Order.Status.CANCELLED},
            Order.Status.CANCELLED: set(),
            Order.Status.DELIVERED: set(),
        }
        if new_status not in Order.Status.values:
            raise ValidationError({'new_status': 'Invalid order status.'})
        if new_status not in valid_transitions.get(order.order_status, set()):
            raise ValidationError({'new_status': f'Cannot transition from {order.order_status} to {new_status}.'})
        with transaction.atomic():
            previous_status = order.order_status
            order.order_status = new_status
            order.save(update_fields=['order_status', 'updated_at'])
            OrderStatusHistory.objects.create(order=order, previous_status=previous_status, new_status=new_status, changed_by=request.user, remarks=remarks)
        return Response(OrderSerializer(order).data)


class OrderItemViewSet(SalesViewSet):
    queryset = OrderItem.objects.select_related('order').all()
    serializer_class = OrderItemSerializer
    write_permissions = {'create': 'CREATE_SALES_ORDER', 'update': 'UPDATE_SALES_ORDER', 'partial_update': 'UPDATE_SALES_ORDER', 'destroy': 'UPDATE_SALES_ORDER'}


class OrderStatusHistoryViewSet(ReadOnlyModelViewSet):
    queryset = OrderStatusHistory.objects.select_related('order', 'changed_by').all()
    serializer_class = OrderStatusHistorySerializer
    permission_classes = [IsAuthenticated]
