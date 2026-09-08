import json
import urllib.error
import urllib.request

import firebase_admin
from django.conf import settings
from firebase_admin import auth, credentials


class FirebaseVerificationError(Exception):
    pass


def _firebase_app():
    if firebase_admin._apps:
        return firebase_admin.get_app()

    service_account_json = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_JSON', '')
    service_account_file = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_FILE', '')
    try:
        if service_account_json:
            credential = credentials.Certificate(json.loads(service_account_json))
        elif service_account_file:
            credential = credentials.Certificate(service_account_file)
        else:
            raise FirebaseVerificationError('Firebase server credentials are not configured.')
        return firebase_admin.initialize_app(credential)
    except FirebaseVerificationError:
        raise
    except Exception as error:
        raise FirebaseVerificationError('Firebase server credentials are invalid.') from error


def _firebase_user(user):
    _firebase_app()
    try:
        if user.firebase_uid:
            try:
                return auth.get_user(user.firebase_uid)
            except auth.UserNotFoundError:
                pass
        return auth.get_user_by_email(user.email)
    except auth.UserNotFoundError:
        return None
    except Exception as error:
        raise FirebaseVerificationError('Firebase account lookup failed.') from error


def _firebase_request(path, payload):
    api_key = getattr(settings, 'FIREBASE_WEB_API_KEY', '')
    if not api_key:
        raise FirebaseVerificationError('Firebase web API key is not configured.')
    request = urllib.request.Request(
        f'https://identitytoolkit.googleapis.com/v1/{path}?key={api_key}',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode('utf-8'))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
        raise FirebaseVerificationError('Firebase verification email could not be sent.') from error


def ensure_firebase_user(user, password):
    firebase_user = _firebase_user(user)
    try:
        if firebase_user is None:
            firebase_user = auth.create_user(
                email=user.email,
                password=password,
                display_name=f'{user.first_name} {user.last_name}'.strip(),
                email_verified=bool(user.email_verified),
            )
        else:
            firebase_user = auth.update_user(
                firebase_user.uid,
                email=user.email,
                password=password,
            )
    except Exception as error:
        raise FirebaseVerificationError('Firebase account could not be prepared.') from error

    if user.firebase_uid != firebase_user.uid:
        user.firebase_uid = firebase_user.uid
        user.save(update_fields=['firebase_uid', 'updated_at'])
    return firebase_user


def send_verification_email(user, password):
    firebase_user = ensure_firebase_user(user, password)
    if firebase_user.email_verified:
        return 'already_verified'
    sign_in = _firebase_request(
        'accounts:signInWithPassword',
        {'email': user.email, 'password': password, 'returnSecureToken': True},
    )
    _firebase_request(
        'accounts:sendOobCode',
        {
            'requestType': 'VERIFY_EMAIL',
            'idToken': sign_in['idToken'],
            **(
                {'continueUrl': settings.FIREBASE_CONTINUE_URL}
                if getattr(settings, 'FIREBASE_CONTINUE_URL', '')
                else {}
            ),
        },
    )
    return 'sent'


def sync_email_verified(user):
    firebase_user = _firebase_user(user)
    if firebase_user is None:
        return user.email_verified
    fields = []
    if user.firebase_uid != firebase_user.uid:
        user.firebase_uid = firebase_user.uid
        fields.append('firebase_uid')
    if firebase_user.email_verified and not user.email_verified:
        user.email_verified = True
        fields.append('email_verified')
    if fields:
        fields.append('updated_at')
        user.save(update_fields=fields)
    return user.email_verified