from django.contrib import admin

from workforce.models import Employee

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import Permission, Role, RolePermission, User


class EmployeeProfileInline(admin.StackedInline):
	model = Employee
	extra = 1
	max_num = 1
	fields = [
		'first_name',
		'last_name',
		'email',
		'phone',
		'department',
		'designation',
		'date_of_birth',
		'gender',
		'address',
		'city',
		'state',
		'pincode',
		'joining_date',
		'employment_type',
		'status',
		'base_salary',
		'profile_photo',
	]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	form = UserAdminChangeForm
	add_form = UserAdminCreationForm
	inlines = [EmployeeProfileInline]
	list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
	list_filter = ['is_active', 'is_staff', 'role']
	search_fields = ['email', 'first_name', 'last_name']
	ordering = ['email']
	fieldsets = [
		(None, {'fields': ['email', 'password']}),
		('Personal information', {'fields': ['first_name', 'last_name', 'phone']}),
		('Access', {'fields': ['role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']}),
	]
	add_fieldsets = [
		(None, {'fields': ['email', 'password1', 'password2']}),
		('Personal information', {'fields': ['first_name', 'last_name', 'phone']}),
		('Access', {'fields': ['role', 'is_active', 'is_staff', 'is_superuser']}),
	]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
	list_display = ['role_name', 'role_code', 'is_active', 'created_at']
	list_filter = ['is_active']
	search_fields = ['role_name', 'role_code']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
	list_display = ['permission_name', 'permission_code', 'module', 'created_at']
	list_filter = ['module']
	search_fields = ['permission_name', 'permission_code', 'module']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
	list_display = ['role', 'permission']
	list_filter = ['role', 'permission__module']
	search_fields = ['role__role_code', 'permission__permission_code']
