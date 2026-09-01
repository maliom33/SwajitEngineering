from rest_framework.routers import DefaultRouter

from .views import DeliveryStatusHistoryViewSet, DeliveryViewSet, DriverViewSet, RouteViewSet, VehicleMaintenanceViewSet, VehicleViewSet

router = DefaultRouter()
router.register('vehicles', VehicleViewSet, basename='logistics-vehicle')
router.register('drivers', DriverViewSet, basename='logistics-driver')
router.register('maintenance', VehicleMaintenanceViewSet, basename='logistics-maintenance')
router.register('routes', RouteViewSet, basename='logistics-route')
router.register('deliveries', DeliveryViewSet, basename='logistics-delivery')
router.register('status-history', DeliveryStatusHistoryViewSet, basename='logistics-status-history')

urlpatterns = router.urls