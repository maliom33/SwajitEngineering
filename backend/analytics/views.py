from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import HasPermission

from .services.dashboard_service import dispatch_analytics, executive_dashboard, finance_analytics, kpis, logistics_analytics, parse_date_filters, recruitment_analytics, sales_analytics, warehouse_analytics, workforce_analytics


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    permission_code = 'VIEW_ANALYTICS'

    def get(self, request):
        try:
            start, end = parse_date_filters(request.query_params)
            data = self.get_data(start, end)
        except ValueError as error:
            return Response({'success': False, 'error': str(error)}, status=400)
        return Response({'success': True, 'data': data, 'filters': {'start_date': start, 'end_date': end}})

    def get_permissions(self):
        self.required_permission = getattr(self, 'permission_code', 'VIEW_ANALYTICS')
        return super().get_permissions()


class ExecutiveDashboardView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = 'VIEW_EXECUTIVE_DASHBOARD'

    def get(self, request):
        return Response({'success': True, 'data': executive_dashboard(), 'filters': {}})


class WorkforceAnalyticsView(AnalyticsView):
    permission_code = 'VIEW_WORKFORCE_ANALYTICS'
    get_data = staticmethod(workforce_analytics)


class RecruitmentAnalyticsView(AnalyticsView):
    permission_code = 'VIEW_RECRUITMENT_ANALYTICS'
    get_data = staticmethod(recruitment_analytics)


class SalesAnalyticsView(AnalyticsView):
    permission_code = 'VIEW_SALES_ANALYTICS'
    get_data = staticmethod(sales_analytics)


class WarehouseAnalyticsView(AnalyticsView):
    permission_code = 'VIEW_WAREHOUSE_ANALYTICS'
    get_data = staticmethod(warehouse_analytics)


class LogisticsAnalyticsView(AnalyticsView):
    permission_code = 'VIEW_LOGISTICS_ANALYTICS'
    get_data = staticmethod(logistics_analytics)


class DispatchAnalyticsView(AnalyticsView):
    permission_code = 'VIEW_DISPATCH_ANALYTICS'
    get_data = staticmethod(dispatch_analytics)


class FinanceAnalyticsView(AnalyticsView):
    permission_code = 'VIEW_FINANCE_ANALYTICS'
    get_data = staticmethod(finance_analytics)


class KpisView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = 'VIEW_ANALYTICS'

    def get(self, request):
        return Response({'success': True, 'data': kpis(), 'filters': {}})
