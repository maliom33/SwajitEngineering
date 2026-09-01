from rest_framework.routers import DefaultRouter

from .views import DeliveryChallanViewSet, DispatchDocumentViewSet, DispatchItemViewSet, DispatchRecordViewSet, DispatchStatusHistoryViewSet

router = DefaultRouter()
router.register('dispatches', DispatchRecordViewSet, basename='dispatch-record')
router.register('dispatch-items', DispatchItemViewSet, basename='dispatch-item')
router.register('challans', DeliveryChallanViewSet, basename='dispatch-challan')
router.register('status-history', DispatchStatusHistoryViewSet, basename='dispatch-status-history')
router.register('documents', DispatchDocumentViewSet, basename='dispatch-document')

urlpatterns = router.urls