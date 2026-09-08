import hashlib

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from accounts.models import EmailVerificationToken


def _token_hash(token):
    return hashlib.sha256(f'{settings.SECRET_KEY}:{token}'.encode()).hexdigest()


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
