from django.core.management import call_command
from django.http import FileResponse, Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django.db import transaction

from accounts.permissions import HasPermission

from .models import (
    Attendance,
    Department,
    Designation,
    Employee,
    EmployeeDocument,
    EmployeeFaceData,
    EmployeePerformance,
    LeaveRequest,
    LeaveType,
    PayrollItem,
    PayrollRun,
    SalaryStructure,
)
from .serializers import (
    AttendanceSerializer,
    DepartmentSerializer,
    DesignationSerializer,
    EmployeeDocumentSerializer,
    EmployeeFaceDataSerializer,
    EmployeePerformanceSerializer,
    EmployeeSerializer,
    LeaveRequestSerializer,
    LeaveTypeSerializer,
    PayrollItemSerializer,
    PayrollRunSerializer,
    SalaryStructureSerializer,
)


class WorkforceViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    write_permissions = {}
    requires_completed_onboarding = True

    def get_permissions(self):
        if (
            getattr(getattr(self.request.user, 'role', None), 'role_code', None) == 'EMPLOYEE'
            and self.requires_completed_onboarding
            and not getattr(getattr(self.request.user, 'employee_profile', None), 'profile_complete', lambda *_: False)(self.request.user)
        ):
            raise PermissionDenied('Please complete email, mobile, password, and profile photo verification first.')
        permission_classes = [IsAuthenticated]
        required_permission = self.write_permissions.get(self.action)
        if required_permission:
            self.required_permission = required_permission
            permission_classes.append(HasPermission)
        return [permission() for permission in permission_classes]


class DepartmentViewSet(WorkforceViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    write_permissions = {'create': 'MANAGE_EMPLOYEES', 'update': 'MANAGE_EMPLOYEES', 'partial_update': 'MANAGE_EMPLOYEES', 'destroy': 'MANAGE_EMPLOYEES'}

    def list(self, request, *args, **kwargs):
        if not Department.objects.exists():
            call_command('seed_departments_designations')
        return super().list(request, *args, **kwargs)


class DesignationViewSet(WorkforceViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    write_permissions = {'create': 'MANAGE_EMPLOYEES', 'update': 'MANAGE_EMPLOYEES', 'partial_update': 'MANAGE_EMPLOYEES', 'destroy': 'MANAGE_EMPLOYEES'}

    def get_queryset(self):
        queryset = super().get_queryset()
        if not queryset.exists():
            call_command('seed_departments_designations')
            queryset = super().get_queryset()
        department_id = self.request.query_params.get('department')
        if department_id:
            return queryset.filter(department_id=department_id)
        return queryset


class EmployeeViewSet(WorkforceViewSet):
    queryset = Employee.objects.select_related('department', 'designation', 'user').all()
    serializer_class = EmployeeSerializer
    write_permissions = {'create': 'MANAGE_EMPLOYEES', 'update': 'MANAGE_EMPLOYEES', 'partial_update': 'MANAGE_EMPLOYEES', 'destroy': 'MANAGE_EMPLOYEES'}
    parser_classes = [FormParser, JSONParser, MultiPartParser]
    requires_completed_onboarding = False

    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(self.request.user.role, 'role_code', None) == 'EMPLOYEE':
            return queryset.filter(user=self.request.user)
        return queryset

    def get_permissions(self):
        if getattr(getattr(self.request.user, 'role', None), 'role_code', None) == 'EMPLOYEE' and self.action in {'retrieve', 'partial_update'}:
            return [IsAuthenticated()]
        return super().get_permissions()


class AttendanceViewSet(WorkforceViewSet):
    queryset = Attendance.objects.select_related('employee').all()
    serializer_class = AttendanceSerializer
    parser_classes = [FormParser, JSONParser, MultiPartParser]
    write_permissions = {'create': 'MANAGE_ATTENDANCE', 'update': 'MANAGE_ATTENDANCE', 'partial_update': 'MANAGE_ATTENDANCE', 'destroy': 'MANAGE_ATTENDANCE'}

    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(self.request.user.role, 'role_code', None) == 'EMPLOYEE':
            return queryset.filter(employee__user=self.request.user)
        return queryset

    def get_permissions(self):
        if getattr(self.request.user.role, 'role_code', None) == 'EMPLOYEE' and self.action in {'list', 'retrieve', 'create'}:
            if self.action == 'create' and not getattr(getattr(self.request.user, 'employee_profile', None), 'profile_complete', lambda *_: False)(self.request.user):
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('Please complete your profile before marking attendance.')
            return [IsAuthenticated()]
        if self.action in {'list', 'retrieve', 'photo'}:
            self.required_permission = 'VIEW_ATTENDANCE'
            return [IsAuthenticated(), HasPermission()]
        return super().get_permissions()

    def perform_create(self, serializer):
        with transaction.atomic():
            employee = serializer.validated_data['employee']
            employee = Employee.objects.select_for_update().get(pk=employee.pk)
            had_attendance = Attendance.objects.filter(employee=employee).exists()
            attendance = serializer.save()
            is_employee_request = getattr(getattr(self.request.user, 'role', None), 'role_code', None) == 'EMPLOYEE'
            is_valid_work_attendance = attendance.status in {
                Attendance.Status.PRESENT,
                Attendance.Status.LATE,
                Attendance.Status.HALF_DAY,
            }
            if (
                is_employee_request
                and employee.user_id == self.request.user.pk
                and employee.status == Employee.Status.INACTIVE
                and not had_attendance
                and is_valid_work_attendance
            ):
                employee.status = Employee.Status.ACTIVE
                employee.save(update_fields=['status', 'updated_at'])

    @action(detail=True, methods=['get'], url_path='photo')
    def photo(self, request, pk=None):
        attendance = self.get_object()
        if not attendance.photo:
            raise Http404
        return FileResponse(attendance.photo.open('rb'), content_type='image/jpeg')


class EmployeeFaceDataViewSet(WorkforceViewSet):
    queryset = EmployeeFaceData.objects.select_related('employee').all()
    serializer_class = EmployeeFaceDataSerializer
    write_permissions = {'create': 'MANAGE_ATTENDANCE', 'update': 'MANAGE_ATTENDANCE', 'partial_update': 'MANAGE_ATTENDANCE', 'destroy': 'MANAGE_ATTENDANCE'}

    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(self.request.user.role, 'role_code', None) == 'EMPLOYEE':
            return queryset.filter(employee__user=self.request.user)
        return queryset

    def get_permissions(self):
        if getattr(self.request.user.role, 'role_code', None) == 'EMPLOYEE' and self.action in {'list', 'retrieve'}:
            return [IsAuthenticated()]
        return super().get_permissions()


class LeaveTypeViewSet(WorkforceViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    write_permissions = {'create': 'MANAGE_ATTENDANCE', 'update': 'MANAGE_ATTENDANCE', 'partial_update': 'MANAGE_ATTENDANCE', 'destroy': 'MANAGE_ATTENDANCE'}


class LeaveRequestViewSet(WorkforceViewSet):
    queryset = LeaveRequest.objects.select_related('employee', 'leave_type', 'approved_by').all()
    serializer_class = LeaveRequestSerializer
    write_permissions = {'create': 'MANAGE_ATTENDANCE', 'update': 'MANAGE_ATTENDANCE', 'partial_update': 'MANAGE_ATTENDANCE', 'destroy': 'MANAGE_ATTENDANCE'}

    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(self.request.user.role, 'role_code', None) == 'EMPLOYEE':
            return queryset.filter(employee__user=self.request.user)
        return queryset

    def get_permissions(self):
        if getattr(self.request.user.role, 'role_code', None) == 'EMPLOYEE' and self.action in {'list', 'retrieve', 'create'}:
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save()


class SalaryStructureViewSet(WorkforceViewSet):
    queryset = SalaryStructure.objects.select_related('employee').all()
    serializer_class = SalaryStructureSerializer
    write_permissions = {'create': 'MANAGE_PAYROLL', 'update': 'MANAGE_PAYROLL', 'partial_update': 'MANAGE_PAYROLL', 'destroy': 'MANAGE_PAYROLL'}

    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(self.request.user.role, 'role_code', None) == 'EMPLOYEE':
            return queryset.filter(employee__user=self.request.user)
        return queryset


class PayrollRunViewSet(WorkforceViewSet):
    queryset = PayrollRun.objects.select_related('processed_by').prefetch_related('items').all()
    serializer_class = PayrollRunSerializer
    write_permissions = {'create': 'MANAGE_PAYROLL', 'update': 'MANAGE_PAYROLL', 'partial_update': 'MANAGE_PAYROLL', 'destroy': 'MANAGE_PAYROLL'}

    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(self.request.user.role, 'role_code', None) == 'EMPLOYEE':
            return queryset.filter(items__employee__user=self.request.user).distinct()
        return queryset


class PayrollItemViewSet(WorkforceViewSet):
    queryset = PayrollItem.objects.select_related('payroll_run', 'employee').all()
    serializer_class = PayrollItemSerializer
    write_permissions = {'create': 'MANAGE_PAYROLL', 'update': 'MANAGE_PAYROLL', 'partial_update': 'MANAGE_PAYROLL', 'destroy': 'MANAGE_PAYROLL'}

    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(self.request.user.role, 'role_code', None) == 'EMPLOYEE':
            return queryset.filter(employee__user=self.request.user)
        return queryset


class EmployeePerformanceViewSet(WorkforceViewSet):
    queryset = EmployeePerformance.objects.select_related('employee', 'evaluated_by').all()
    serializer_class = EmployeePerformanceSerializer
    write_permissions = {'create': 'MANAGE_PERFORMANCE', 'update': 'MANAGE_PERFORMANCE', 'partial_update': 'MANAGE_PERFORMANCE', 'destroy': 'MANAGE_PERFORMANCE'}


class EmployeeDocumentViewSet(WorkforceViewSet):
    queryset = EmployeeDocument.objects.select_related('employee', 'uploaded_by', 'verified_by').all()
    serializer_class = EmployeeDocumentSerializer
    write_permissions = {'create': 'MANAGE_EMPLOYEES', 'update': 'MANAGE_EMPLOYEES', 'partial_update': 'MANAGE_EMPLOYEES', 'destroy': 'MANAGE_EMPLOYEES'}
