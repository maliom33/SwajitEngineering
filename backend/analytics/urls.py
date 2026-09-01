from django.urls import path

from .views import DispatchAnalyticsView, ExecutiveDashboardView, FinanceAnalyticsView, KpisView, LogisticsAnalyticsView, RecruitmentAnalyticsView, SalesAnalyticsView, WarehouseAnalyticsView, WorkforceAnalyticsView

urlpatterns = [
    path('executive-dashboard/', ExecutiveDashboardView.as_view(), name='analytics-executive-dashboard'),
    path('workforce/', WorkforceAnalyticsView.as_view(), name='analytics-workforce'),
    path('recruitment/', RecruitmentAnalyticsView.as_view(), name='analytics-recruitment'),
    path('sales/', SalesAnalyticsView.as_view(), name='analytics-sales'),
    path('warehouse/', WarehouseAnalyticsView.as_view(), name='analytics-warehouse'),
    path('logistics/', LogisticsAnalyticsView.as_view(), name='analytics-logistics'),
    path('dispatch/', DispatchAnalyticsView.as_view(), name='analytics-dispatch'),
    path('finance/', FinanceAnalyticsView.as_view(), name='analytics-finance'),
    path('kpis/', KpisView.as_view(), name='analytics-kpis'),
]