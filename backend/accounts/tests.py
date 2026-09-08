from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta
from rest_framework.test import APITestCase
from unittest.mock import patch
from types import SimpleNamespace

from .models import Permission, Role, RolePermission, User


class AuthenticationAndRBACTests(APITestCase):
	def setUp(self):
		cache.clear()
		self.role = Role.objects.create(role_name='System Administrator', role_code='SYSTEM_ADMIN')
		self.permission = Permission.objects.create(
			permission_name='Manage Users',
			permission_code='MANAGE_USERS',
			module='accounts',
		)
		RolePermission.objects.create(role=self.role, permission=self.permission)
		self.user = User.objects.create_user(
			email='admin@example.com',
			password='SecurePassword123!',
			first_name='Admin',
			last_name='User',
			role=self.role,
		)

	def test_password_is_hashed_and_email_is_normalized(self):
		self.assertNotEqual(self.user.password, 'SecurePassword123!')
		self.assertTrue(self.user.check_password('SecurePassword123!'))
		self.assertEqual(self.user.email, 'admin@example.com')

	def test_role_permission_relation_is_unique(self):
		self.assertEqual(self.role.role_permissions.count(), 1)
		self.assertEqual(self.permission.role_permissions.count(), 1)

	def test_login_returns_tokens_and_user_role(self):
		response = self.client.post(reverse('auth-login'), {
			'email': 'ADMIN@example.com',
			'password': 'SecurePassword123!',
		}, format='json')

		self.assertEqual(response.status_code, 200)
		self.assertIn('access', response.data)
		self.assertIn('refresh', response.data)
		self.assertEqual(response.data['user']['role_code'], 'SYSTEM_ADMIN')
		self.assertEqual(response.data['user']['permissions'], ['MANAGE_USERS'])
		self.assertNotIn('password', response.data['user'])

	def test_me_requires_authentication(self):
		response = self.client.get(reverse('auth-me'))
		self.assertEqual(response.status_code, 401)

	def test_me_returns_authenticated_user(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.get(reverse('auth-me'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['email'], self.user.email)
		self.assertEqual(response.data['role'], 'System Administrator')

	def test_unverified_employee_login_is_allowed(self):
		employee_role, _ = Role.objects.get_or_create(role_code='EMPLOYEE', defaults={'role_name': 'Employee'})
		User.objects.create_user(email='employee@example.com', password='SecurePassword123!', role=employee_role)
		response = self.client.post(reverse('auth-login'), {'email': 'employee@example.com', 'password': 'SecurePassword123!'}, format='json')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['user']['role_code'], 'EMPLOYEE')

	def test_email_link_verification_is_one_time_and_does_not_change_employment_status(self):
		employee_role, _ = Role.objects.get_or_create(role_code='EMPLOYEE', defaults={'role_name': 'Employee'})
		employee = User.objects.create_user(email='employee@example.com', password='SecurePassword123!', role=employee_role)
		from workforce.models import Employee, Department, Designation
		department = Department.objects.create(department_name='Verification Operations')
		designation = Designation.objects.create(designation_name='Verification Employee')
		profile = Employee.objects.create(user=employee, first_name='Email', last_name='Employee', email=employee.email, phone='+919876543210', gender='Other', department=department, designation=designation, joining_date='2026-01-01', employment_type='FULL_TIME', base_salary='1000.00', status=Employee.Status.INACTIVE)
		self.client.force_authenticate(user=employee)
		from accounts.models import EmailVerificationToken
		self.assertEqual(EmailVerificationToken.objects.count(), 0)
		with patch('accounts.views.send_verification_email') as deliver:
			response = self.client.post(reverse('auth-email-verification-request'), {'password': 'SecurePassword123!'}, format='json')
		self.assertEqual(response.status_code, 200)
		deliver.assert_called_once_with(employee, 'SecurePassword123!')
		self.assertEqual(EmailVerificationToken.objects.count(), 0)
		from accounts.services.email_verification_service import _token_hash
		import secrets
		token = secrets.token_urlsafe(32)
		EmailVerificationToken.objects.create(user=employee, token_hash=_token_hash(token), expires_at=timezone.now() + timedelta(hours=1))
		verify = self.client.get(reverse('auth-email-verification-link') + f'?token={token}')
		self.assertEqual(verify.status_code, 200)
		employee.refresh_from_db()
		profile.refresh_from_db()
		self.assertTrue(employee.email_verified)
		self.assertEqual(profile.status, Employee.Status.INACTIVE)
		reused = self.client.get(reverse('auth-email-verification-link') + f'?token={token}')
		self.assertEqual(reused.status_code, 200)

	def test_verification_request_requires_authentication(self):
		response = self.client.post(reverse('auth-email-verification-request'), {'password': 'SecurePassword123!'}, format='json')
		self.assertEqual(response.status_code, 401)

	def test_authenticated_employee_can_resend_only_for_self(self):
		employee_role, _ = Role.objects.get_or_create(role_code='EMPLOYEE', defaults={'role_name': 'Employee'})
		from workforce.models import Employee, Department, Designation
		department = Department.objects.create(department_name='Resend Operations')
		designation = Designation.objects.create(designation_name='Resend Employee')
		user = User.objects.create_user(email='resend@example.com', password='SecurePassword123!', role=employee_role)
		Employee.objects.create(user=user, employee_code='EMP-RESEND', first_name='Resend', last_name='Employee', email=user.email, phone='+919876543210', gender='Other', department=department, designation=designation, joining_date='2026-01-01', employment_type='FULL_TIME', base_salary='1000.00')
		other_user = User.objects.create_user(email='other@example.com', password='OtherPassword123!', role=employee_role)
		Employee.objects.create(user=other_user, employee_code='EMP-OTHER', first_name='Other', last_name='Employee', email=other_user.email, phone='+919876543212', gender='Other', department=department, designation=designation, joining_date='2026-01-01', employment_type='FULL_TIME', base_salary='1000.00')
		self.client.force_authenticate(user=user)
		with patch('accounts.views.send_verification_email') as deliver:
			response = self.client.post(reverse('auth-email-verification-request'), {'email': other_user.email, 'employee_code': 'EMP-OTHER', 'password': 'SecurePassword123!'}, format='json')
		self.assertEqual(response.status_code, 200)
		deliver.assert_called_once_with(user, 'SecurePassword123!')

	def test_verification_requests_are_throttled(self):
		employee_role, _ = Role.objects.get_or_create(role_code='EMPLOYEE', defaults={'role_name': 'Employee'})
		from workforce.models import Employee, Department, Designation
		department = Department.objects.create(department_name='Throttle Operations')
		designation = Designation.objects.create(designation_name='Throttle Employee')
		user = User.objects.create_user(email='throttle@example.com', password='SecurePassword123!', role=employee_role)
		Employee.objects.create(user=user, first_name='Throttle', last_name='Employee', email=user.email, phone='+919876543213', gender='Other', department=department, designation=designation, joining_date='2026-01-01', employment_type='FULL_TIME', base_salary='1000.00')
		self.client.force_authenticate(user=user)
		with patch('accounts.views.send_verification_email'):
			responses = [
				self.client.post(reverse('auth-email-verification-request'), {'password': 'SecurePassword123!'}, format='json')
				for _ in range(4)
			]
		self.assertEqual([response.status_code for response in responses], [200, 200, 200, 429])

	def test_firebase_sync_marks_email_verified_without_activating_employee(self):
		from accounts.services.firebase_verification_service import sync_email_verified
		from workforce.models import Employee, Department, Designation
		employee_role, _ = Role.objects.get_or_create(role_code='EMPLOYEE', defaults={'role_name': 'Employee'})
		user = User.objects.create_user(email='firebase@example.com', password='SecurePassword123!', role=employee_role)
		department = Department.objects.create(department_name='Firebase Operations')
		designation = Designation.objects.create(designation_name='Firebase Employee')
		profile = Employee.objects.create(user=user, first_name='Firebase', last_name='Employee', email=user.email, phone='+919876543211', gender='Other', department=department, designation=designation, joining_date='2026-01-01', employment_type='FULL_TIME', base_salary='1000.00', status=Employee.Status.INACTIVE)
		with patch('accounts.services.firebase_verification_service._firebase_user', return_value=SimpleNamespace(uid='firebase-uid', email_verified=True)):
			self.assertTrue(sync_email_verified(user))
		user.refresh_from_db()
		profile.refresh_from_db()
		self.assertTrue(user.email_verified)
		self.assertEqual(user.firebase_uid, 'firebase-uid')
		self.assertEqual(profile.status, Employee.Status.INACTIVE)

	def test_firebase_invalid_or_missing_user_does_not_change_state(self):
		from accounts.services.firebase_verification_service import sync_email_verified
		with patch('accounts.services.firebase_verification_service._firebase_user', return_value=None):
			self.assertFalse(sync_email_verified(self.user))
		self.user.refresh_from_db()
		self.assertFalse(self.user.email_verified)

	def test_firebase_already_verified_user_does_not_receive_duplicate_email(self):
		from accounts.services.firebase_verification_service import send_verification_email
		with patch('accounts.services.firebase_verification_service.ensure_firebase_user', return_value=SimpleNamespace(uid='firebase-uid', email_verified=True)):
			self.assertEqual(send_verification_email(self.user, 'SecurePassword123!'), 'already_verified')


	def test_email_password_values_are_normalized_for_smtp(self):
		from config.settings import _normalize_email_setting
		self.assertEqual(_normalize_email_setting('uukx ayem yqui ejwd'), 'uukxayemyquiejwd')
		self.assertEqual(_normalize_email_setting('  swajeet51@gmail.com  '), 'swajeet51@gmail.com')

	def test_password_reset_request_sends_email_for_existing_user(self):
		with patch('accounts.services.password_reset_service.send_mail') as deliver:
			response = self.client.post(reverse('auth-password-reset-request'), {'email': self.user.email}, format='json')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(deliver.called)
		self.assertIn('password reset', deliver.call_args.args[1].lower())

	def test_password_reset_confirm_updates_password(self):
		from django.contrib.auth.tokens import PasswordResetTokenGenerator
		from django.utils.http import urlsafe_base64_encode
		from django.utils.encoding import force_bytes

		token = PasswordResetTokenGenerator().make_token(self.user)
		uid = urlsafe_base64_encode(force_bytes(self.user.pk))
		response = self.client.post(reverse('auth-password-reset-confirm'), {
			'uidb64': uid,
			'token': token,
			'password': 'NewSecurePassword456!',
			'confirm_password': 'NewSecurePassword456!',
		}, format='json')

		self.assertEqual(response.status_code, 200)
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('NewSecurePassword456!'))
