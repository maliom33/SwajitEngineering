import hashlib
import secrets
from datetime import timedelta
from smtplib import SMTPException
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class PasswordResetError(Exception):
    pass


def _configured(value):
    return bool(value and not value.startswith('change-me'))


def _password_reset_url(user, token):
    reset_frontend_url = getattr(settings, 'PASSWORD_RESET_URL', '').strip()
    if not reset_frontend_url:
        raise PasswordResetError('Password reset frontend URL is not configured.')
    params = {'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': token}
    return f'{reset_frontend_url}?{urlencode(params)}'


def issue_password_reset_email(user):
    required = (
        getattr(settings, 'EMAIL_HOST', ''),
        getattr(settings, 'EMAIL_HOST_USER', ''),
        getattr(settings, 'EMAIL_HOST_PASSWORD', ''),
        getattr(settings, 'DEFAULT_FROM_EMAIL', ''),
        getattr(settings, 'PASSWORD_RESET_URL', ''),
    )
    if not all(_configured(value) for value in required):
        raise PasswordResetError('Email provider or password reset URL is not configured.')

    token = PasswordResetTokenGenerator().make_token(user)
    try:
        send_mail(
            'Password reset for your Swajit Engineering account',
            f'Use this link to complete your password reset: {_password_reset_url(user, token)}\nThis link is valid for a limited time.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except (OSError, SMTPException) as error:
        raise PasswordResetError('Email provider is unavailable. Check SMTP settings and try again.') from error
    return token
