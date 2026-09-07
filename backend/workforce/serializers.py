import hashlib
import re
import secrets
from datetime import timedelta

from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.db import transaction
from rest_framework import serializers

from accounts.models import Role, User
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


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=['Male', 'Female', 'Other', 'Prefer not to say'])
    profile_photo = serializers.ImageField(required=False, allow_null=True)
    activation_token = serializers.SerializerMethodField(read_only=True)
    activation_email_sent = serializers.SerializerMethodField(read_only=True)
    email_verified = serializers.SerializerMethodField(read_only=True)
    phone_verified = serializers.SerializerMethodField(read_only=True)
    profile_complete = serializers.SerializerMethodField(read_only=True)
    department_name = serializers.SerializerMethodField(read_only=True)
    designation_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            field.name for field in Employee._meta.fields
            if field.name not in {'activation_token_hash', 'activation_expires_at'}
        ] + ['activation_token', 'activation_email_sent', 'email_verified', 'phone_verified', 'profile_complete', 'department_name', 'designation_name']
        read_only_fields = ['employee_code', 'user', 'activation_token_hash', 'activation_expires_at']

    def get_activation_token(self, employee):
        return getattr(employee, '_activation_token', None)

    def get_activation_email_sent(self, employee):
        return bool(getattr(employee, '_activation_email_sent', False))

    def get_email_verified(self, employee):
        return bool(employee.user and employee.user.email_verified)

    def get_phone_verified(self, employee):
        return bool(employee.user and employee.user.phone_verified)

    def get_profile_complete(self, employee):
        return employee.profile_complete()

    def get_department_name(self, employee):
        return employee.department.department_name if employee.department else None

    def get_designation_name(self, employee):
        return employee.designation.designation_name if employee.designation else None

    def validate_profile_photo(self, photo):
        if photo.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Profile photo must be 5 MB or smaller.')
        return photo

    def validate(self, attrs):
        email = attrs.get('email', getattr(self.instance, 'email', None))
        if email:
            existing_user = User.objects.filter(email__iexact=email).exclude(
                pk=getattr(getattr(self.instance, 'user', None), 'pk', None)
            ).exists()
            existing_employee = Employee.objects.filter(email__iexact=email).exclude(pk=getattr(self.instance, 'pk', None)).exists()
            if existing_user or existing_employee:
                raise serializers.ValidationError({'email': 'An employee or user with this email already exists.'})
        phone = attrs.get('phone', getattr(self.instance, 'phone', None))
        if phone:
            digits = re.sub(r'\D', '', phone)
            if digits.startswith('91') and len(digits) == 12:
                digits = digits[2:]
            if len(digits) != 10 or digits[0] not in '6789':
                raise serializers.ValidationError({'phone': 'Enter a valid Indian mobile number.'})
            current_user_id = getattr(getattr(self.instance, 'user', None), 'pk', None)
            current_employee_id = getattr(self.instance, 'pk', None)
            if User.objects.filter(phone__regex=r'[^0-9]*' + digits + r'[^0-9]*').exclude(pk=current_user_id).exists() or Employee.objects.filter(phone__regex=r'[^0-9]*' + digits + r'[^0-9]*').exclude(pk=current_employee_id).exists():
                raise serializers.ValidationError({'phone': 'An employee or user with this mobile number already exists.'})
        department = attrs.get('department', getattr(self.instance, 'department', None))
        designation = attrs.get('designation', getattr(self.instance, 'designation', None))
        if designation and designation.department_id and department and designation.department_id != department.department_id:
            raise serializers.ValidationError({'designation': 'This designation does not belong to the selected department.'})
        return attrs

    def update(self, instance, validated_data):
        user = self.context.get('request').user if self.context.get('request') else None
        if getattr(getattr(user, 'role', None), 'role_code', None) == 'EMPLOYEE':
            allowed = {'first_name', 'last_name', 'email', 'phone', 'gender', 'address', 'city', 'state', 'pincode', 'profile_photo'}
            validated_data = {key: value for key, value in validated_data.items() if key in allowed}
        employee = super().update(instance, validated_data)
        if employee.user and any(field in validated_data for field in ('first_name', 'last_name', 'email', 'phone')):
            employee.user.first_name = employee.first_name
            employee.user.last_name = employee.last_name
            employee.user.email = employee.email
            employee.user.phone = employee.phone
            update_fields = ['first_name', 'last_name', 'email', 'phone']
            if 'email' in validated_data:
                employee.user.email_verified = False
                update_fields.append('email_verified')
            if 'phone' in validated_data:
                employee.user.phone_verified = False
                update_fields.append('phone_verified')
            employee.user.save(update_fields=update_fields)
        return employee

    def create(self, validated_data):
        with transaction.atomic():
            validated_data['status'] = Employee.Status.INACTIVE
            role = Role.objects.get(role_code='EMPLOYEE')
            user = User.objects.create_user(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                phone=validated_data['phone'],
                role=role,
                is_active=False,
                password=None,
            )
            user.is_first_login = True
            user.save(update_fields=['is_first_login'])
            employee = Employee.objects.create(user=user, **validated_data)
            activation_token = secrets.token_urlsafe(32)
            employee.activation_token_hash = hashlib.sha256(activation_token.encode()).hexdigest()
            employee.activation_expires_at = timezone.now() + timedelta(days=7)
            employee.save(update_fields=['activation_token_hash', 'activation_expires_at'])
            employee._activation_token = activation_token
            return employee


class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
    photo = serializers.ImageField(required=False, allow_null=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    status = serializers.ChoiceField(choices=Attendance.Status.choices, required=False)
    photo_available = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attendance
        fields = [field.name for field in Attendance._meta.fields] + ['photo_available']
        read_only_fields = ['employee', 'attendance_date', 'check_in', 'check_out', 'created_at', 'updated_at', 'photo_available']

    def get_photo_available(self, attendance):
        return bool(attendance.photo)

    def validate(self, attrs):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if getattr(getattr(user, 'role', None), 'role_code', None) == 'EMPLOYEE':
            if self.instance is not None:
                raise serializers.ValidationError('Employees cannot modify attendance records.')
            attrs['employee'] = user.employee_profile
            attrs['attendance_date'] = timezone.localdate()
            attrs['status'] = Attendance.Status.PRESENT
            attrs['check_in'] = timezone.now()
            attrs['check_out'] = None
            attrs['attendance_method'] = Attendance.AttendanceMethod.MANUAL
            if not attrs.get('photo'):
                raise serializers.ValidationError({'photo': 'A camera photo is required.'})
            if attrs.get('latitude') is None or attrs.get('longitude') is None:
                raise serializers.ValidationError({'location': 'Current location is required.'})
        elif not attrs.get('employee'):
            raise serializers.ValidationError({'employee': 'Employee is required.'})
        if attrs.get('attendance_date') and Attendance.objects.filter(employee=attrs['employee'], attendance_date=attrs['attendance_date']).exists():
            raise serializers.ValidationError({'attendance_date': 'Attendance already marked for today.'})
        return attrs


class EmployeeFaceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeFaceData
        fields = ['face_data_id', 'employee', 'model_version', 'registered_at', 'is_active']
        read_only_fields = fields


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)

    class Meta:
        model = LeaveRequest
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        if getattr(getattr(getattr(request, 'user', None), 'role', None), 'role_code', None) == 'EMPLOYEE':
            attrs['employee'] = request.user.employee_profile
        elif not attrs.get('employee'):
            raise serializers.ValidationError({'employee': 'Employee is required.'})
        if attrs['end_date'] < attrs['start_date']:
            raise serializers.ValidationError({'end_date': 'End date cannot be before start date.'})
        return attrs


class SalaryStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryStructure
        fields = '__all__'


class PayrollRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollRun
        fields = '__all__'


class PayrollItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollItem
        fields = '__all__'


class EmployeePerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePerformance
        fields = '__all__'


class EmployeeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDocument
        fields = '__all__'