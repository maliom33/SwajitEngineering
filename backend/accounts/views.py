import hashlib
import hmac

from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User
from .serializers import (
    ActivationSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    UserInfoSerializer,
)
from .services.email_verification_service import EmailVerificationError, issue_verification_email, verify_email_token
from .services.password_reset_service import PasswordResetError, issue_password_reset_email


class EmployeeActivationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from workforce.models import Employee
        serializer = ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        token = serializer.validated_data['activation_token']
        password = serializer.validated_data['password']

        with transaction.atomic():
            employee = Employee.objects.select_for_update().select_related('user').filter(
                email=email, user__isnull=False
            ).first()
            if not employee or not employee.activation_token_hash:
                raise serializers.ValidationError({'detail': 'This account has already been activated or the activation link is invalid.'})
            if not employee.activation_expires_at or employee.activation_expires_at < timezone.now():
                raise serializers.ValidationError({'detail': 'This activation link is invalid or expired.'})
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            if not hmac.compare_digest(employee.activation_token_hash, token_hash):
                raise serializers.ValidationError({'detail': 'This activation link is invalid or expired.'})

            employee.user.set_password(password)
            employee.user.is_active = True
            employee.user.is_first_login = True
            employee.user.save(update_fields=['password', 'is_active', 'is_first_login'])
            employee.activation_token_hash = ''
            employee.activation_expires_at = None
            employee.save(update_fields=['activation_token_hash', 'activation_expires_at'])
        try:
            issue_verification_email(employee.user)
        except EmailVerificationError as error:
            return Response({'detail': f'Account setup completed, but the verification email could not be sent: {error}'}, status=503)

        return Response({'detail': 'Account setup successful. Please check your email and click the verification link before logging in.'})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access, refresh = serializer.create_tokens()
        return Response({
            'access': access,
            'refresh': refresh,
            'user': UserInfoSerializer(serializer.validated_data['user']).data,
        })


class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserInfoSerializer(request.user).data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.is_first_login = False
        request.user.save(update_fields=['password', 'is_first_login'])
        return Response({'detail': 'Password changed successfully.'})


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            try:
                issue_password_reset_email(user)
            except PasswordResetError as error:
                return Response({'detail': str(error)}, status=503)
        return Response({'detail': 'If an account exists for this email, a password reset link has been sent.'})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = str(serializer.validated_data['uidb64']).strip()
        token = str(serializer.validated_data['token']).strip()
        password = serializer.validated_data['password']

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({'detail': 'This password reset link is invalid.'})

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({'detail': 'This password reset link is invalid or expired.'})

        user.set_password(password)
        user.is_first_login = False
        user.save(update_fields=['password', 'is_first_login', 'updated_at'])
        return Response({'detail': 'Password reset successfully.'})


class EmailVerificationRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from workforce.models import Employee
        email = str(request.data.get('email', '')).strip().lower()
        employee_code = str(request.data.get('employee_code', '')).strip()
        user = getattr(request, 'user', None)
        if not getattr(user, 'is_authenticated', False):
            user = User.objects.filter(email=email, employee_profile__employee_code=employee_code).first()
        if not user or getattr(getattr(user, 'role', None), 'role_code', None) != 'EMPLOYEE' or user.email_verified:
            return Response({'detail': 'If the account is eligible, a verification link will be sent.'})
        try:
            issue_verification_email(user)
        except EmailVerificationError as error:
            return Response({'detail': str(error)}, status=503)
        return Response({'detail': 'Verification link sent.'})


class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = str(request.query_params.get('token', '')).strip()
        result = verify_email_token(token)
        messages = {
            'verified': ('Email verified successfully. You can now log in.', 200),
            'already_verified': ('Email is already verified.', 200),
            'expired': ('This email verification link has expired.', 400),
            'used': ('This email verification link has already been used.', 400),
            'invalid': ('This email verification link is invalid.', 400),
        }
        message, status_code = messages[result]
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            color = '#176b5b' if result in {'verified', 'already_verified'} else '#9b2c2c'
            body = f'<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>Email verification</title></head><body style="font-family:Arial,sans-serif;max-width:560px;margin:64px auto;padding:24px;color:#172b2b"><h1 style="color:{color}">Email verification</h1><p>{message}</p></body></html>'
            return HttpResponse(body, status=status_code)
        return Response({'detail': message}, status=status_code)


