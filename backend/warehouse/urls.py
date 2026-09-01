from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AllocateOrderStockView,
    InventoryViewSet,
    LowStockView,
    ProductCategoryViewSet,
    ProductViewSet,
    PurchaseOrderItemViewSet,
    PurchaseOrderViewSet,
    ReleaseOrderStockView,
    ReserveOrderStockView,
    StockTransactionViewSet,
    StockTransferItemViewSet,
    StockTransferViewSet,
    SupplierViewSet,
    WarehouseLocationViewSet,
)

router = DefaultRouter()
router.register('warehouses', WarehouseLocationViewSet, basename='warehouse-location')
router.register('categories', ProductCategoryViewSet, basename='warehouse-category')
router.register('products', ProductViewSet, basename='warehouse-product')
router.register('suppliers', SupplierViewSet, basename='warehouse-supplier')
router.register('inventory', InventoryViewSet, basename='warehouse-inventory')
router.register('stock-transactions', StockTransactionViewSet, basename='warehouse-stock-transaction')
router.register('purchase-orders', PurchaseOrderViewSet, basename='warehouse-purchase-order')
router.register('purchase-order-items', PurchaseOrderItemViewSet, basename='warehouse-purchase-order-item')
router.register('stock-transfers', StockTransferViewSet, basename='warehouse-stock-transfer')
router.register('stock-transfer-items', StockTransferItemViewSet, basename='warehouse-stock-transfer-item')

urlpatterns = router.urls + [
    path('low-stock/', LowStockView.as_view(), name='warehouse-low-stock'),
    path('orders/<int:order_id>/reserve-stock/', ReserveOrderStockView.as_view(), name='warehouse-order-reserve-stock'),
    path('orders/<int:order_id>/release-stock/', ReleaseOrderStockView.as_view(), name='warehouse-order-release-stock'),
    path('orders/<int:order_id>/allocate-stock/', AllocateOrderStockView.as_view(), name='warehouse-order-allocate-stock'),
]