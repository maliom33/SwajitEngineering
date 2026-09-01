from rest_framework.routers import DefaultRouter

from .views import (
    CustomerCommunicationViewSet,
    CustomerViewSet,
    OrderItemViewSet,
    OrderStatusHistoryViewSet,
    OrderViewSet,
    QuotationItemViewSet,
    QuotationViewSet,
)

router = DefaultRouter()
router.register('customers', CustomerViewSet, basename='sales-customer')
router.register('communications', CustomerCommunicationViewSet, basename='sales-communication')
router.register('quotations', QuotationViewSet, basename='sales-quotation')
router.register('quotation-items', QuotationItemViewSet, basename='sales-quotation-item')
router.register('orders', OrderViewSet, basename='sales-order')
router.register('order-items', OrderItemViewSet, basename='sales-order-item')
router.register('status-history', OrderStatusHistoryViewSet, basename='sales-status-history')

urlpatterns = router.urls