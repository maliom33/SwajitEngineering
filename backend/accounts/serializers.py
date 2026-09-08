from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        attrs['email'] = User.objects.normalize_email(attrs['email'])
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Invalid email or password.')
        if not user.is_active:
            raise serializers.ValidationError('This account is inactive.')
        attrs['user'] = user
        return attrs

    def create_tokens(self):
        user = self.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token), str(refresh)


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_token = serializers.CharField(trim_whitespace=False)
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    confirm_password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})

        attrs['email'] = User.objects.normalize_email(attrs['email'])
        try:
            validate_password(attrs['password'])
        except ValidationError as error:
            raise serializers.ValidationError({'password': error.messages}) from error
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, trim_whitespace=False)
    new_password = serializers.CharField(write_only=True, trim_whitespace=False)
    confirm_password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['current_password']):
            raise serializers.ValidationError({'current_password': 'Current password is incorrect.'})
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        if attrs['new_password'] == attrs['current_password']:
            raise serializers.ValidationError({'new_password': 'New password must be different.'})
        validate_password(attrs['new_password'], user)
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return User.objects.normalize_email(value)


class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(trim_whitespace=False)
    token = serializers.CharField(trim_whitespace=False)
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    confirm_password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        try:
            validate_password(attrs['password'])
        except ValidationError as error:
            raise serializers.ValidationError({'password': error.messages}) from error
        return attrs


class UserInfoSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.role_name', allow_null=True, read_only=True)
    role_code = serializers.CharField(source='role.role_code', allow_null=True, read_only=True)
    permissions = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'role_code', 'permissions', 'is_first_login', 'email_verified', 'phone_verified', 'employee']
        read_only_fields = fields

    def get_permissions(self, user):
        if not user.role:
            return []
        return list(
            user.role.role_permissions.filter(permission__isnull=False)
            .values_list('permission__permission_code', flat=True)
        )

    def get_employee(self, user):
        employee = getattr(user, 'employee_profile', None)
        if not employee:
            return None
        profile_photo = None
        if employee.profile_photo:
            profile_photo = employee.profile_photo.url
            request = self.context.get('request')
            if request:
                profile_photo = request.build_absolute_uri(profile_photo)
        return {
            'employee_id': employee.employee_id,
            'employee_code': employee.employee_code,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'email': employee.email,
            'phone': employee.phone,
            'joining_date': employee.joining_date,
            'employment_type': employee.employment_type,
            'gender': employee.gender,
            'status': employee.status,
            'department': employee.department_id,
            'department_name': employee.department.department_name,
            'designation': employee.designation_id,
            'designation_name': employee.designation.designation_name,
			'profile_complete': employee.profile_complete(user),
            'profile_photo': profile_photo,
        }