from smtplib import SMTPException
from urllib.parse import urlencode

from django.conf import settings
from django.core.mail import send_mail


class ActivationEmailError(Exception):
    pass


def issue_activation_email(user, activation_token):
    required = (
        getattr(settings, 'EMAIL_HOST', ''),
        getattr(settings, 'EMAIL_HOST_USER', ''),
        getattr(settings, 'EMAIL_HOST_PASSWORD', ''),
        getattr(settings, 'DEFAULT_FROM_EMAIL', ''),
        getattr(settings, 'EMPLOYEE_ACTIVATION_URL', ''),
    )
    if not all(required):
        raise ActivationEmailError('Email provider or employee activation URL is not configured.')

    separator = '&' if '?' in settings.EMPLOYEE_ACTIVATION_URL else '?'
    activation_url = f'{settings.EMPLOYEE_ACTIVATION_URL}{separator}{urlencode({"email": user.email, "activation_token": activation_token})}'
    try:
        send_mail(
            'Activate your Swajit Engineering employee account',
            f'Use this link to activate your employee account: {activation_url}\nThis link expires in 7 days.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except (OSError, SMTPException) as error:
        raise ActivationEmailError('Email provider is unavailable. Use the activation link shown to HR and check SMTP settings.') from error