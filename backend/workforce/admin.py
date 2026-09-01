from django.contrib import admin

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


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	list_display = ['department_name', 'is_active', 'created_at']
	list_filter = ['is_active']
	search_fields = ['department_name']


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
	list_display = ['designation_name', 'is_active', 'created_at']
	list_filter = ['is_active']
	search_fields = ['designation_name']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ['employee_code', 'first_name', 'last_name', 'department', 'designation', 'status', 'joining_date']
	list_filter = ['status', 'employment_type', 'department', 'designation']
	search_fields = ['employee_code', 'first_name', 'last_name', 'email']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
	list_display = ['employee', 'attendance_date', 'status', 'attendance_method', 'check_in', 'check_out']
	list_filter = ['status', 'attendance_method', 'attendance_date']
	search_fields = ['employee__employee_code', 'employee__email']


@admin.register(EmployeeFaceData)
class EmployeeFaceDataAdmin(admin.ModelAdmin):
	list_display = ['employee', 'model_version', 'registered_at', 'is_active']
	list_filter = ['is_active', 'model_version']
	search_fields = ['employee__employee_code']
	exclude = ['face_encoding_reference']


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
	list_display = ['leave_name', 'maximum_days', 'is_paid', 'is_active']
	list_filter = ['is_paid', 'is_active']
	search_fields = ['leave_name']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
	list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'status', 'approved_by']
	list_filter = ['status', 'leave_type']
	search_fields = ['employee__employee_code', 'employee__email']


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
	list_display = ['employee', 'effective_from', 'effective_to', 'basic_salary']
	list_filter = ['effective_from']
	search_fields = ['employee__employee_code', 'employee__email']


@admin.register(PayrollRun)
class PayrollRunAdmin(admin.ModelAdmin):
	list_display = ['period_start', 'period_end', 'status', 'processed_date', 'processed_by']
	list_filter = ['status', 'period_start']
	search_fields = ['processed_by__email']


@admin.register(PayrollItem)
class PayrollItemAdmin(admin.ModelAdmin):
	list_display = ['payroll_run', 'employee', 'gross_salary', 'net_salary', 'payment_status', 'payment_date']
	list_filter = ['payment_status', 'payment_date']
	search_fields = ['employee__employee_code', 'employee__email']


@admin.register(EmployeePerformance)
class EmployeePerformanceAdmin(admin.ModelAdmin):
	list_display = ['employee', 'evaluation_period_start', 'evaluation_period_end', 'overall_score', 'evaluated_by']
	list_filter = ['evaluation_period_end']
	search_fields = ['employee__employee_code', 'employee__email', 'evaluated_by__email']


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
	list_display = ['employee', 'document_type', 'document_name', 'is_verified', 'uploaded_at', 'expiry_date']
	list_filter = ['document_type', 'is_verified', 'expiry_date']
	search_fields = ['employee__employee_code', 'document_name']
