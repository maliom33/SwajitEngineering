from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch

from .models import Permission, Role, RolePermission, User


class AuthenticationAndRBACTests(APITestCase):
	def setUp(self):
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

	def test_unverified_employee_login_is_rejected(self):
		employee_role, _ = Role.objects.get_or_create(role_code='EMPLOYEE', defaults={'role_name': 'Employee'})
		User.objects.create_user(email='employee@example.com', password='SecurePassword123!', role=employee_role)
		response = self.client.post(reverse('auth-login'), {'email': 'employee@example.com', 'password': 'SecurePassword123!'}, format='json')
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data['non_field_errors'][0], 'Please verify your email before logging in.')

	def test_email_link_verification_is_one_time_and_does_not_change_employment_status(self):
		employee_role, _ = Role.objects.get_or_create(role_code='EMPLOYEE', defaults={'role_name': 'Employee'})
		employee = User.objects.create_user(email='employee@example.com', password='SecurePassword123!', role=employee_role)
		from workforce.models import Employee, Department, Designation
		department = Department.objects.create(department_name='Verification Operations')
		designation = Designation.objects.create(designation_name='Verification Employee')
		profile = Employee.objects.create(user=employee, first_name='Email', last_name='Employee', email=employee.email, phone='+919876543210', gender='Other', department=department, designation=designation, joining_date='2026-01-01', employment_type='FULL_TIME', base_salary='1000.00', status=Employee.Status.INACTIVE)
		self.client.force_authenticate(user=employee)
		with patch('accounts.services.email_verification_service.send_mail') as deliver:
			response = self.client.post(reverse('auth-email-verification-request'))
		self.assertEqual(response.status_code, 200)
		message = deliver.call_args.args[1]
		token = message.split('?token=', 1)[1].split('\n', 1)[0]
		verify = self.client.get(reverse('auth-email-verification-link') + f'?token={token}')
		self.assertEqual(verify.status_code, 200)
		employee.refresh_from_db()
		profile.refresh_from_db()
		self.assertTrue(employee.email_verified)
		self.assertEqual(profile.status, Employee.Status.INACTIVE)
		reused = self.client.get(reverse('auth-email-verification-link') + f'?token={token}')
		self.assertEqual(reused.status_code, 200)

	def test_unverified_employee_can_resend_with_email_and_employee_code(self):
		employee_role, _ = Role.objects.get_or_create(role_code='EMPLOYEE', defaults={'role_name': 'Employee'})
		from workforce.models import Employee, Department, Designation
		department = Department.objects.create(department_name='Resend Operations')
		designation = Designation.objects.create(designation_name='Resend Employee')
		user = User.objects.create_user(email='resend@example.com', password='SecurePassword123!', role=employee_role)
		Employee.objects.create(user=user, employee_code='EMP-RESEND', first_name='Resend', last_name='Employee', email=user.email, phone='+919876543210', gender='Other', department=department, designation=designation, joining_date='2026-01-01', employment_type='FULL_TIME', base_salary='1000.00')
		with patch('accounts.services.email_verification_service.send_mail') as deliver:
			response = self.client.post(reverse('auth-email-verification-request'), {'email': user.email, 'employee_code': 'EMP-RESEND'}, format='json')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(deliver.called)

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
