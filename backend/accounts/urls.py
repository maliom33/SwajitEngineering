from django.urls import path

from .views import (
    ChangePasswordView,
    EmployeeActivationView,
    EmailVerificationRequestView,
    EmailVerificationView,
    LoginView,
    MeView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RefreshView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth-login'),
    path('refresh/', RefreshView.as_view(), name='auth-refresh'),
    path('me/', MeView.as_view(), name='auth-me'),
    path('change-password/', ChangePasswordView.as_view(), name='auth-change-password'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='auth-password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='auth-password-reset-confirm'),
    path('activate/', EmployeeActivationView.as_view(), name='auth-activate'),
    path('verification/email/request/', EmailVerificationRequestView.as_view(), name='auth-email-verification-request'),
    path('verification/email/verify/', EmailVerificationView.as_view(), name='auth-email-verification-link'),
]