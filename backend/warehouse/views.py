from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from accounts.permissions import HasPermission
from sales.models import Order

from .models import Inventory, Product, ProductCategory, PurchaseOrder, PurchaseOrderItem, StockTransaction, StockTransfer, StockTransferItem, Supplier, Warehouse
from .serializers import (
    InventorySerializer, ProductCategorySerializer, ProductSerializer, PurchaseOrderItemSerializer,
    PurchaseOrderSerializer, StockTransactionSerializer, StockTransferItemSerializer,
    StockTransferSerializer, SupplierSerializer, WarehouseSerializer,
)
from .services.inventory import (
    allocate_stock_for_order, adjust_inventory, low_stock_inventory, receive_purchase_order,
    receive_stock_transfer, release_reserved_stock, reserve_stock_for_order, transfer_stock,
)


class WarehouseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    write_permissions = {}

    def get_permissions(self):
        permissions = [IsAuthenticated]
        required = self.write_permissions.get(self.action) or getattr(self, 'action_permissions', {}).get(self.action)
        if required:
            self.required_permission = required
            permissions.append(HasPermission)
        return [permission() for permission in permissions]


class WarehouseEntityViewSet(WarehouseViewSet):
    write_permissions = {'create': 'MANAGE_WAREHOUSES', 'update': 'MANAGE_WAREHOUSES', 'partial_update': 'MANAGE_WAREHOUSES', 'destroy': 'MANAGE_WAREHOUSES'}


class WarehouseModelViewSet(WarehouseViewSet):
    write_permission = None

    def get_permissions(self):
        self.write_permissions = {action: self.write_permission for action in ['create', 'update', 'partial_update', 'destroy'] if self.write_permission}
        return super().get_permissions()


class WarehouseLocationViewSet(WarehouseEntityViewSet):
    queryset = Warehouse.objects.select_related('manager').all()
    serializer_class = WarehouseSerializer


class ProductCategoryViewSet(WarehouseModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    write_permission = 'MANAGE_PRODUCTS'


class ProductViewSet(WarehouseModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    write_permission = 'MANAGE_PRODUCTS'


class SupplierViewSet(WarehouseModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    write_permission = 'MANAGE_SUPPLIERS'


class InventoryViewSet(ReadOnlyModelViewSet):
    queryset = Inventory.objects.select_related('warehouse', 'product').all()
    serializer_class = InventorySerializer

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action == 'adjust':
            permissions.append(HasPermission)
            self.required_permission = 'ADJUST_INVENTORY'
        return [permission() for permission in permissions]

    @action(detail=True, methods=['post'], url_path='adjust')
    def adjust(self, request, pk=None):
        inventory = self.get_object()
        quantity_delta = request.data.get('quantity_delta')
        reason = request.data.get('reason', 'OTHER')
        remarks = request.data.get('remarks', '')
        if quantity_delta is None:
            return Response({'detail': 'quantity_delta is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            adjust_inventory(inventory, quantity_delta=quantity_delta, performed_by=request.user, reason=reason, remarks=remarks)
        except (ValueError, TypeError) as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(InventorySerializer(Inventory.objects.get(pk=inventory.pk)).data)


class StockTransactionViewSet(ReadOnlyModelViewSet):
    queryset = StockTransaction.objects.select_related('warehouse', 'product', 'performed_by').all()
    serializer_class = StockTransactionSerializer
    permission_classes = [IsAuthenticated]


class PurchaseOrderViewSet(WarehouseModelViewSet):
    queryset = PurchaseOrder.objects.select_related('supplier', 'warehouse', 'created_by', 'approved_by').prefetch_related('items').all()
    serializer_class = PurchaseOrderSerializer
    write_permission = 'MANAGE_PURCHASE_ORDERS'
    action_permissions = {'receive': 'RECEIVE_STOCK'}

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='receive')
    def receive(self, request, pk=None):
        purchase_order = self.get_object()
        received_quantities = request.data.get('received_quantities', {})
        try:
            result = receive_purchase_order(purchase_order, received_quantities, request.user)
        except ValueError as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(PurchaseOrderSerializer(result).data)


class PurchaseOrderItemViewSet(WarehouseModelViewSet):
    queryset = PurchaseOrderItem.objects.select_related('purchase_order', 'product').all()
    serializer_class = PurchaseOrderItemSerializer
    write_permission = 'MANAGE_PURCHASE_ORDERS'


class StockTransferViewSet(WarehouseModelViewSet):
    queryset = StockTransfer.objects.select_related('source_warehouse', 'destination_warehouse', 'initiated_by', 'approved_by').prefetch_related('items').all()
    serializer_class = StockTransferSerializer
    write_permission = 'MANAGE_STOCK_TRANSFERS'
    action_permissions = {'approve': 'MANAGE_STOCK_TRANSFERS', 'receive': 'MANAGE_STOCK_TRANSFERS'}

    def perform_create(self, serializer):
        serializer.save(initiated_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        transfer = self.get_object()
        if transfer.status not in [StockTransfer.Status.DRAFT, StockTransfer.Status.REQUESTED]:
            return Response({'detail': 'Only draft or requested transfers can be approved.'}, status=status.HTTP_400_BAD_REQUEST)
        transfer.status = StockTransfer.Status.APPROVED
        transfer.approved_by = request.user
        transfer.save(update_fields=['status', 'approved_by', 'updated_at'])
        return Response(StockTransferSerializer(transfer).data)

    @action(detail=True, methods=['post'], url_path='start')
    def start(self, request, pk=None):
        try:
            transfer = transfer_stock(self.get_object(), request.user)
        except ValueError as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(StockTransferSerializer(transfer).data)

    @action(detail=True, methods=['post'], url_path='receive')
    def receive(self, request, pk=None):
        try:
            transfer = receive_stock_transfer(self.get_object(), request.user)
        except ValueError as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(StockTransferSerializer(transfer).data)


class StockTransferItemViewSet(WarehouseModelViewSet):
    queryset = StockTransferItem.objects.select_related('transfer', 'product').all()
    serializer_class = StockTransferItemSerializer
    write_permission = 'MANAGE_STOCK_TRANSFERS'


class LowStockView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = 'VIEW_INVENTORY'

    def get(self, request):
        data = [
            {'warehouse': item.warehouse.warehouse_code, 'product': item.product.sku, 'available_quantity': item.available_quantity, 'reorder_level': item.reorder_level, 'reorder_quantity': item.product.reorder_quantity, 'status': 'LOW_STOCK'}
            for item in low_stock_inventory()
        ]
        return Response(data)


class OrderStockOperationView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = 'ALLOCATE_STOCK'

    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        warehouse_id = request.data.get('warehouse_id')
        warehouse = get_object_or_404(Warehouse, pk=warehouse_id) if warehouse_id else None
        if self.operation == 'reserve' and warehouse is None:
            return Response({'detail': 'warehouse_id is required for stock reservation.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if self.operation == 'reserve':
                result = reserve_stock_for_order(order, warehouse, request.user)
            elif self.operation == 'release':
                result = release_reserved_stock(order, request.user)
            else:
                result = allocate_stock_for_order(order, request.user)
        except ValueError as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': result.status if result else 'RELEASED'})


class ReserveOrderStockView(OrderStockOperationView):
    operation = 'reserve'


class ReleaseOrderStockView(OrderStockOperationView):
    operation = 'release'


class AllocateOrderStockView(OrderStockOperationView):
    operation = 'allocate'
