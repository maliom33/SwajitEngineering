import hashlib
import secrets
from datetime import timedelta
from smtplib import SMTPException
from urllib.parse import urlencode

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from accounts.models import EmailVerificationToken


class EmailVerificationError(Exception):
    pass


def _configured(value):
    return bool(value and not value.startswith('change-me'))


def _token_hash(token):
    return hashlib.sha256(f'{settings.SECRET_KEY}:{token}'.encode()).hexdigest()


def _verification_url(token):
    base_url = getattr(settings, 'EMAIL_VERIFICATION_URL', '').strip()
    separator = '&' if '?' in base_url else '?'
    return f'{base_url}{separator}{urlencode({"token": token})}'


def issue_verification_email(user):
    required = (
        getattr(settings, 'EMAIL_HOST', ''),
        getattr(settings, 'EMAIL_HOST_USER', ''),
        getattr(settings, 'EMAIL_HOST_PASSWORD', ''),
        getattr(settings, 'DEFAULT_FROM_EMAIL', ''),
        getattr(settings, 'EMAIL_VERIFICATION_URL', ''),
    )
    if not all(_configured(value) for value in required):
        raise EmailVerificationError('Email provider or verification URL is not configured.')

    token = secrets.token_urlsafe(32)
    now = timezone.now()
    with transaction.atomic():
        EmailVerificationToken.objects.filter(user=user, used_at__isnull=True).update(used_at=now)
        verification = EmailVerificationToken.objects.create(
            user=user,
            token_hash=_token_hash(token),
            expires_at=now + timedelta(hours=24),
        )
    try:
        send_mail(
            'Verify your Swajit Engineering employee account',
            f'Use this link to verify your email: {_verification_url(token)}\nThis link expires in 24 hours.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except (OSError, SMTPException) as error:
        raise EmailVerificationError('Email provider is unavailable. Check SMTP settings and try again.') from error
    return verification


def verify_email_token(token):
    if not token:
        return 'invalid'
    token_hash = _token_hash(token)
    with transaction.atomic():
        verification = EmailVerificationToken.objects.select_for_update().select_related('user').filter(token_hash=token_hash).first()
        if not verification:
            return 'invalid'
        if verification.user.email_verified:
            return 'already_verified'
        if verification.used_at is not None:
            return 'used'
        if verification.is_expired():
            return 'expired'
        verification.used_at = timezone.now()
        verification.save(update_fields=['used_at'])
        verification.user.email_verified = True
        verification.user.save(update_fields=['email_verified', 'updated_at'])
    return 'verified'
