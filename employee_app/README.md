# Swajit Engineering Employee Mobile App

This Flutter application is a real employee client for the existing Django REST API. It does not connect directly to PostgreSQL and does not create a second employee database.

## Environment

- Flutter 3.38.5
- Dart 3.10.4
- Existing Django backend and PostgreSQL database

Install dependencies and analyze the app:

```powershell
flutter pub get
flutter analyze
flutter test
```

## Run

Start the existing backend first:

```powershell
cd backend
..\.venv\Scripts\Activate.ps1
python manage.py runserver 0.0.0.0:8000
```

Then run the mobile app from `employee_app`:

```powershell
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000/api/
```

`10.0.2.2` is for the Android emulator. For a physical device, use the development computer's LAN IP, for example:

```powershell
flutter run --dart-define=API_BASE_URL=http://192.168.1.20:8000/api/
```

The device and computer must be on the same network, and the backend must listen on `0.0.0.0:8000`.

## Login and activation

HR creates the employee through the existing React HR application. Django creates the inactive linked User with role `EMPLOYEE` and returns a one-time activation token. The employee activates the account through the existing web activation flow at `/activate`, then signs in to this Flutter app with email and password.

The app calls `/api/auth/login/`, verifies `role_code == EMPLOYEE`, then calls `/api/auth/me/`. Non-employee accounts are rejected. Access and refresh tokens are stored in `flutter_secure_storage`; expired access tokens are refreshed through `/api/auth/refresh/` and failed sessions are cleared.

## Connected modules

- Dashboard and employee identity from `/api/auth/me/`
- Profile from the linked employee identity
- Attendance history from `/api/workforce/attendance/`
- Leave types from `/api/workforce/leave-types/`
- Submit and view own leave requests through `/api/workforce/leave-requests/`
- Secure logout by clearing local tokens

## Verification configuration

Email verification uses a secure, expiring, one-time Django verification link. Set `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`, and `EMAIL_VERIFICATION_URL` in `backend/.env`.

Mobile numbers are normal employee profile fields. The application does not send SMS and does not use Firebase Phone Authentication or email OTPs.

## Current limitations

- A real SMTP provider and public verification URL are required for email verification.
- Forgot-password is not enabled because the backend has no password-reset API.
- Payroll is not shown because the existing payroll APIs are management-oriented and do not provide an employee-scoped response. No unsafe payroll exposure was added.
- Attendance self-marking is not presented because the existing backend workflow is not a dedicated employee punch API.

## API and database architecture

```text
Flutter employee app -> Django REST API -> Django ORM -> existing PostgreSQL
```

The app reuses the existing `accounts.User`, `workforce.Employee`, `Department`, `Designation`, `Attendance`, `LeaveType`, and `LeaveRequest` data. No Flutter-side business records are created.

## Production notes

Use HTTPS, a deployed API URL, secure Android network policy, proper secret management, and a dedicated employee-scoped payroll API before production deployment.# employee_app

A new Flutter project.

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.
