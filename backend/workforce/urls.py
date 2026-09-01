from rest_framework.routers import DefaultRouter

from .views import (
    AttendanceViewSet,
    DepartmentViewSet,
    DesignationViewSet,
    EmployeeDocumentViewSet,
    EmployeeFaceDataViewSet,
    EmployeePerformanceViewSet,
    EmployeeViewSet,
    LeaveRequestViewSet,
    LeaveTypeViewSet,
    PayrollItemViewSet,
    PayrollRunViewSet,
    SalaryStructureViewSet,
)

router = DefaultRouter()
router.register('departments', DepartmentViewSet, basename='department')
router.register('designations', DesignationViewSet, basename='designation')
router.register('employees', EmployeeViewSet, basename='employee')
router.register('attendance', AttendanceViewSet, basename='attendance')
router.register('face-data', EmployeeFaceDataViewSet, basename='face-data')
router.register('leave-types', LeaveTypeViewSet, basename='leave-type')
router.register('leave-requests', LeaveRequestViewSet, basename='leave-request')
router.register('salary-structures', SalaryStructureViewSet, basename='salary-structure')
router.register('payroll-runs', PayrollRunViewSet, basename='payroll-run')
router.register('payroll-items', PayrollItemViewSet, basename='payroll-item')
router.register('performance', EmployeePerformanceViewSet, basename='performance')
router.register('documents', EmployeeDocumentViewSet, basename='document')

urlpatterns = router.urls