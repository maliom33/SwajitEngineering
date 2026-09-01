import base64
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch

from accounts.models import Permission, Role, RolePermission, User

from .models import (
	Attendance,
	Department,
	Designation,
	Employee,
	EmployeeCodeSequence,
	LeaveRequest,
	LeaveType,
	PayrollItem,
	PayrollRun,
)


class WorkforceModelTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			email='hr@example.com',
			password='SecurePassword123!',
			first_name='HR',
			last_name='Manager',
		)
		role = Role.objects.create(role_name='HR Manager', role_code='HR_MANAGER')
		permission, _ = Permission.objects.get_or_create(
			permission_code='MANAGE_EMPLOYEES',
			defaults={
				'permission_name': 'Manage employees',
				'module': 'workforce',
			},
		)
		RolePermission.objects.create(role=role, permission=permission)
		for permission_code, permission_name in (
			('VIEW_ATTENDANCE', 'View attendance'),
			('VIEW_PAYROLL', 'View payroll'),
			('MANAGE_PAYROLL', 'Manage payroll'),
		):
			workflow_permission, _ = Permission.objects.get_or_create(
				permission_code=permission_code,
				defaults={'permission_name': permission_name, 'module': 'workforce'},
			)
			RolePermission.objects.create(role=role, permission=workflow_permission)
		self.user.role = role
		self.user.save(update_fields=['role'])
		self.client.force_authenticate(user=self.user)
		self.department = Department.objects.create(department_name='Operations')
		self.designation = Designation.objects.create(designation_name='Driver')
		self.employee = Employee.objects.create(
			user=self.user,
			employee_code='EMP-001',
			first_name='Asha',
			last_name='Shah',
			email='asha@example.com',
			phone='1234567890',
			department=self.department,
			designation=self.designation,
			joining_date=date(2026, 1, 1),
			employment_type=Employee.EmploymentType.FULL_TIME,
			base_salary=Decimal('50000.00'),
		)

	def test_department_creation(self):
		self.assertEqual(str(self.department), 'Operations')
		self.assertEqual(Department.objects.count(), 1)

	def test_designation_creation(self):
		self.assertEqual(str(self.designation), 'Driver')

	def test_employee_and_user_relationship(self):
		self.assertIs(self.employee.user, self.user)
		self.assertIs(self.user.employee_profile, self.employee)

	def test_duplicate_employee_code_is_rejected(self):
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Employee.objects.create(
					employee_code='EMP-001',
					first_name='Duplicate',
					last_name='Employee',
					email='duplicate@example.com',
					phone='0000000000',
					department=self.department,
					designation=self.designation,
					joining_date=date(2026, 1, 2),
					employment_type=Employee.EmploymentType.CONTRACT,
					base_salary=Decimal('10000.00'),
				)

	def test_employee_code_is_generated_when_omitted(self):
		new_employee = Employee.objects.create(
			first_name='Generated',
			last_name='Employee',
			email='generated@example.com',
			phone='0000000001',
			department=self.department,
			designation=self.designation,
			joining_date=date(2026, 1, 3),
			employment_type=Employee.EmploymentType.CONTRACT,
			base_salary=Decimal('10000.00'),
		)
		self.assertEqual(new_employee.employee_code, 'EMP001')

	def test_employee_code_sequence_does_not_reuse_after_delete(self):
		first = Employee.objects.create(
			first_name='First', last_name='Generated', email='first@example.com', phone='0000000002',
			department=self.department, designation=self.designation, joining_date=date(2026, 1, 4),
			employment_type=Employee.EmploymentType.CONTRACT, base_salary=Decimal('10000.00'),
		)
		self.assertEqual(first.employee_code, 'EMP001')
		first.delete()
		second = Employee.objects.create(
			first_name='Second', last_name='Generated', email='second@example.com', phone='0000000003',
			department=self.department, designation=self.designation, joining_date=date(2026, 1, 5),
			employment_type=Employee.EmploymentType.CONTRACT, base_salary=Decimal('10000.00'),
		)
		self.assertEqual(second.employee_code, 'EMP002')

	def test_employee_serializer_does_not_require_employee_code(self):
		from .serializers import EmployeeSerializer

		serializer = EmployeeSerializer(data={
			'first_name': 'API', 'last_name': 'Employee', 'email': 'api@example.com', 'phone': '9000000004',
			'gender': 'Other',
			'department': self.department.pk, 'designation': self.designation.pk, 'joining_date': '2026-01-06',
			'employment_type': Employee.EmploymentType.FULL_TIME, 'base_salary': '10000.00',
		})
		self.assertTrue(serializer.is_valid(), serializer.errors)

	def test_employee_serializer_rejects_invalid_gender(self):
		from .serializers import EmployeeSerializer

		serializer = EmployeeSerializer(data={
			'first_name': 'API', 'last_name': 'Employee', 'email': 'api-invalid@example.com', 'phone': '9000000005',
			'gender': 'Unknown',
			'department': self.department.pk, 'designation': self.designation.pk, 'joining_date': '2026-01-07',
			'employment_type': Employee.EmploymentType.FULL_TIME, 'base_salary': '10000.00',
		})
		self.assertFalse(serializer.is_valid())
		self.assertIn('gender', serializer.errors)

	def test_designation_api_filters_by_department(self):
		other_department = Department.objects.create(department_name='Warehouse')
		other_designation = Designation.objects.create(designation_name='Warehouse Assistant', department=other_department)
		response = self.client.get(reverse('designation-list'), {'department': self.department.pk})
		self.assertEqual(response.status_code, 200)
		self.assertNotIn(other_designation.pk, [item['designation_id'] for item in response.data])

	def test_employee_serializer_rejects_designation_from_another_department(self):
		other_department = Department.objects.create(department_name='Warehouse')
		other_designation = Designation.objects.create(designation_name='Warehouse Assistant', department=other_department)
		from .serializers import EmployeeSerializer

		serializer = EmployeeSerializer(data={
			'first_name': 'Mismatch', 'last_name': 'Employee', 'email': 'mismatch@example.com', 'phone': '9000000009',
			'gender': 'Male', 'department': self.department.pk, 'designation': other_designation.pk,
			'joining_date': '2026-01-11', 'employment_type': Employee.EmploymentType.FULL_TIME, 'base_salary': '10000.00',
		})
		self.assertFalse(serializer.is_valid())
		self.assertIn('designation', serializer.errors)

	def test_employee_api_generates_code_and_preserves_it_on_patch(self):
		response = self.client.post(reverse('employee-list'), {
			'first_name': 'Created', 'last_name': 'Employee', 'email': 'created@example.com', 'phone': '9000000006',
			'gender': 'Female', 'department': self.department.pk, 'designation': self.designation.pk,
			'joining_date': '2026-01-08', 'employment_type': Employee.EmploymentType.FULL_TIME,
			'base_salary': '12000.00',
		}, format='json')
		self.assertEqual(response.status_code, 201, response.data)
		self.assertEqual(response.data['employee_code'], 'EMP001')
		self.assertEqual(response.data['gender'], 'Female')
		self.assertNotIn('activation_token_hash', response.data)
		self.assertNotIn('activation_expires_at', response.data)

		patch_response = self.client.patch(
			reverse('employee-detail', args=[response.data['employee_id']]),
			{'employee_code': 'EMP999', 'gender': 'Other'},
			format='json',
		)
		self.assertEqual(patch_response.status_code, 200, patch_response.data)
		self.assertEqual(patch_response.data['employee_code'], 'EMP001')
		self.assertEqual(patch_response.data['gender'], 'Other')

	def test_hr_manager_has_employee_management_permission(self):
		self.assertTrue(self.user.role.role_permissions.filter(permission__permission_code='MANAGE_EMPLOYEES').exists())

	def test_employee_role_cannot_manage_employee_records(self):
		employee_role, _ = Role.objects.get_or_create(role_code='EMPLOYEE', defaults={'role_name': 'Employee'})
		employee_user = User.objects.create_user(
			email='employee@example.com', password='SecurePassword123!', role=employee_role,
		)
		self.client.force_authenticate(user=employee_user)
		response = self.client.post(reverse('employee-list'), {}, format='json')
		self.assertEqual(response.status_code, 403)

	def test_employee_creation_creates_activation_account_and_login(self):
		response = self.client.post(reverse('employee-list'), {
			'first_name': 'Portal', 'last_name': 'Employee', 'email': 'portal@example.com', 'phone': '9000000007',
			'gender': 'Male', 'department': self.department.pk, 'designation': self.designation.pk,
			'joining_date': '2026-01-09', 'employment_type': Employee.EmploymentType.FULL_TIME,
			'base_salary': '12000.00',
		}, format='json')
		self.assertEqual(response.status_code, 201, response.data)
		created_employee = Employee.objects.get(pk=response.data['employee_id'])
		self.assertEqual(created_employee.user.role.role_code, 'EMPLOYEE')
		self.assertFalse(created_employee.user.is_active)
		self.assertTrue(response.data['activation_token'])

		with patch('accounts.views.issue_verification_email'):
			activation = self.client.post(reverse('auth-activate'), {
				'email': 'portal@example.com',
				'activation_token': response.data['activation_token'],
				'password': 'NewSecurePassword123!',
				'confirm_password': 'NewSecurePassword123!',
			}, format='json')
		self.assertEqual(activation.status_code, 200, activation.data)
		created_employee.user.refresh_from_db()
		created_employee.refresh_from_db()
		self.assertTrue(created_employee.user.is_active)
		self.assertTrue(created_employee.user.check_password('NewSecurePassword123!'))
		self.assertEqual(created_employee.status, Employee.Status.INACTIVE)
		self.assertFalse(created_employee.activation_token_hash)
		self.assertIsNone(created_employee.activation_expires_at)

		login = self.client.post(reverse('auth-login'), {'email': 'portal@example.com', 'password': 'NewSecurePassword123!'}, format='json')
		self.assertEqual(login.status_code, 400, login.data)
		created_employee.user.email_verified = True
		created_employee.user.save(update_fields=['email_verified'])
		login = self.client.post(reverse('auth-login'), {'email': 'portal@example.com', 'password': 'NewSecurePassword123!'}, format='json')
		self.assertEqual(login.status_code, 200, login.data)
		self.assertEqual(login.data['user']['role_code'], 'EMPLOYEE')
		self.assertEqual(login.data['user']['employee']['employee_code'], created_employee.employee_code)

		reused_token = self.client.post(reverse('auth-activate'), {
			'email': 'portal@example.com',
			'activation_token': response.data['activation_token'],
			'password': 'AnotherSecurePassword123!',
			'confirm_password': 'AnotherSecurePassword123!',
		}, format='json')
		self.assertEqual(reused_token.status_code, 400)

	def test_activation_rejects_mismatched_or_weak_passwords(self):
		response = self.client.post(reverse('employee-list'), {
			'first_name': 'Validation', 'last_name': 'Employee', 'email': 'validation@example.com', 'phone': '9000000008',
			'gender': 'Other', 'department': self.department.pk, 'designation': self.designation.pk,
			'joining_date': '2026-01-10', 'employment_type': Employee.EmploymentType.FULL_TIME,
			'base_salary': '12000.00',
		}, format='json')
		self.assertEqual(response.status_code, 201, response.data)

		mismatch = self.client.post(reverse('auth-activate'), {
			'email': 'validation@example.com', 'activation_token': response.data['activation_token'],
			'password': 'SecurePassword123!', 'confirm_password': 'DifferentPassword123!',
		}, format='json')
		self.assertEqual(mismatch.status_code, 400)
		self.assertIn('confirm_password', mismatch.data)

		weak = self.client.post(reverse('auth-activate'), {
			'email': 'validation@example.com', 'activation_token': response.data['activation_token'],
			'password': 'password', 'confirm_password': 'password',
		}, format='json')
		self.assertEqual(weak.status_code, 400)
		self.assertIn('password', weak.data)

	def test_employee_attendance_is_limited_to_authenticated_profile(self):
		portal_user = User.objects.create_user(email='portal@example.com', password='SecurePassword123!', role=Role.objects.get(role_code='EMPLOYEE'))
		portal_employee = Employee.objects.create(
			user=portal_user, first_name='Portal', last_name='Employee', email=portal_user.email, phone='0000000008',
			gender='Other', department=self.department, designation=self.designation, joining_date=date(2026, 1, 10),
			employment_type=Employee.EmploymentType.FULL_TIME, base_salary=Decimal('12000.00'),
		)
		Attendance.objects.create(employee=portal_employee, attendance_date=date(2026, 4, 1), status=Attendance.Status.PRESENT)
		Attendance.objects.create(employee=self.employee, attendance_date=date(2026, 4, 1), status=Attendance.Status.ABSENT)
		self.client.force_authenticate(user=portal_user)
		response = self.client.get(reverse('attendance-list'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual([record['employee'] for record in response.data], [portal_employee.employee_id])

	def test_hr_can_view_attendance_but_cannot_write_it(self):
		Attendance.objects.create(
			employee=self.employee,
			attendance_date=date(2026, 4, 2),
			status=Attendance.Status.PRESENT,
		)
		list_response = self.client.get(reverse('attendance-list'))
		self.assertEqual(list_response.status_code, 200)

		create_response = self.client.post(reverse('attendance-list'), {
			'employee': self.employee.employee_id,
			'attendance_date': '2026-04-03',
			'status': Attendance.Status.PRESENT,
		}, format='json')
		self.assertEqual(create_response.status_code, 403)

	def test_employee_attendance_requires_photo_and_location(self):
		employee_role = Role.objects.get(role_code='EMPLOYEE')
		employee_user = User.objects.create_user(
			email='attendance@example.com', password='SecurePassword123!', role=employee_role,
		)
		employee = Employee.objects.create(
			user=employee_user, first_name='Attendance', last_name='Employee', email=employee_user.email,
			phone='1234567891', department=self.department, designation=self.designation,
			joining_date=date(2026, 1, 12), employment_type=Employee.EmploymentType.FULL_TIME,
			base_salary=Decimal('12000.00'),
		)
		self.client.force_authenticate(user=employee_user)
		response = self.client.post(reverse('attendance-list'), {
			'employee': employee.employee_id,
			'attendance_date': '2026-04-03',
			'status': Attendance.Status.PRESENT,
			'attendance_method': Attendance.AttendanceMethod.FACE_RECOGNITION,
		}, format='json')
		self.assertEqual(response.status_code, 403)
		self.assertFalse(Attendance.objects.filter(employee=employee).exists())

	def test_profile_completion_requires_verification_flags(self):
		employee_role = Role.objects.get(role_code='EMPLOYEE')
		employee_user = User.objects.create_user(
			email='complete@example.com', password='SecurePassword123!', role=employee_role,
			is_first_login=False, email_verified=True, phone_verified=True,
		)
		employee = Employee.objects.create(
			user=employee_user, first_name='Complete', last_name='Employee', email=employee_user.email,
			phone='1234567894', gender='Other', department=self.department, designation=self.designation,
			joining_date=date(2026, 1, 15), employment_type=Employee.EmploymentType.FULL_TIME,
			base_salary=Decimal('14000.00'), profile_photo=SimpleUploadedFile('profile.png', b'profile'),
		)
		self.assertTrue(employee.profile_complete(employee_user))

	def test_employee_can_submit_photo_and_location_attendance(self):
		employee_role = Role.objects.get(role_code='EMPLOYEE')
		employee_user = User.objects.create_user(
			email='capture@example.com', password='SecurePassword123!', role=employee_role,
		)
		employee_user.is_first_login = False
		employee_user.email_verified = True
		employee_user.phone_verified = True
		employee_user.save(update_fields=['is_first_login', 'email_verified', 'phone_verified'])
		image_bytes = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=')
		employee = Employee.objects.create(
			user=employee_user, first_name='Capture', last_name='Employee', email=employee_user.email,
			phone='1234567893', gender='Other', department=self.department, designation=self.designation,
			joining_date=date(2026, 1, 14), employment_type=Employee.EmploymentType.FULL_TIME,
			base_salary=Decimal('14000.00'), profile_photo=SimpleUploadedFile('profile.png', image_bytes, content_type='image/png'),
		)
		self.client.force_authenticate(user=employee_user)
		response = self.client.post(reverse('attendance-list'), {
			'photo': SimpleUploadedFile('attendance.png', image_bytes, content_type='image/png'),
			'latitude': '19.876543',
			'longitude': '75.123456',
		}, format='multipart')
		self.assertEqual(response.status_code, 201, response.data)
		self.assertEqual(response.data['employee'], employee.employee_id)
		self.assertEqual(response.data['latitude'], '19.876543')
		self.assertTrue(response.data['photo_available'])
		employee.refresh_from_db()
		self.assertEqual(employee.status, Employee.Status.ACTIVE)

	def test_employee_payroll_is_limited_to_authenticated_profile(self):
		employee_role = Role.objects.get(role_code='EMPLOYEE')
		other_user = User.objects.create_user(
			email='payroll@example.com', password='SecurePassword123!', role=employee_role,
			is_first_login=False, email_verified=True, phone_verified=True,
		)
		other_employee = Employee.objects.create(
			user=other_user, first_name='Payroll', last_name='Employee', email=other_user.email,
			phone='1234567892', department=self.department, designation=self.designation,
			joining_date=date(2026, 1, 13), employment_type=Employee.EmploymentType.FULL_TIME,
			base_salary=Decimal('13000.00'), gender='Other', profile_photo=SimpleUploadedFile('payroll.png', b'profile'),
		)
		payroll_run = PayrollRun.objects.create(period_start=date(2026, 2, 1), period_end=date(2026, 2, 28))
		PayrollItem.objects.create(
			payroll_run=payroll_run, employee=self.employee, basic_salary=Decimal('50000.00'),
			gross_salary=Decimal('52000.00'), net_salary=Decimal('48000.00'),
		)
		PayrollItem.objects.create(
			payroll_run=payroll_run, employee=other_employee, basic_salary=Decimal('13000.00'),
			gross_salary=Decimal('13000.00'), net_salary=Decimal('13000.00'),
		)
		self.client.force_authenticate(user=other_user)
		items = self.client.get(reverse('payroll-item-list'))
		runs = self.client.get(reverse('payroll-run-list'))
		self.assertEqual(items.status_code, 200)
		self.assertEqual(runs.status_code, 200)
		self.assertEqual([item['employee'] for item in items.data], [other_employee.employee_id])
		self.assertEqual([run['payroll_run_id'] for run in runs.data], [payroll_run.payroll_run_id])

	def test_attendance_unique_per_employee_and_date(self):
		Attendance.objects.create(
			employee=self.employee,
			attendance_date=date(2026, 2, 1),
			status=Attendance.Status.PRESENT,
		)
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Attendance.objects.create(
					employee=self.employee,
					attendance_date=date(2026, 2, 1),
					status=Attendance.Status.LATE,
				)

	def test_leave_dates_are_validated(self):
		leave_request = LeaveRequest(
			employee=self.employee,
			leave_type=LeaveType.objects.create(leave_name='Casual', maximum_days=10),
			start_date=date(2026, 3, 10),
			end_date=date(2026, 3, 9),
			total_days=Decimal('1'),
			reason='Invalid date range',
		)
		with self.assertRaises(ValidationError):
			leave_request.full_clean()

	def test_payroll_uses_decimal_fields_and_unique_employee_item(self):
		payroll_run = PayrollRun.objects.create(
			period_start=date(2026, 2, 1),
			period_end=date(2026, 2, 28),
		)
		item = PayrollItem.objects.create(
			payroll_run=payroll_run,
			employee=self.employee,
			basic_salary=Decimal('50000.00'),
			gross_salary=Decimal('52000.00'),
			net_salary=Decimal('48000.00'),
		)
		self.assertIsInstance(item.net_salary, Decimal)
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				PayrollItem.objects.create(
					payroll_run=payroll_run,
					employee=self.employee,
					basic_salary=Decimal('50000.00'),
					gross_salary=Decimal('52000.00'),
					net_salary=Decimal('48000.00'),
				)

	def test_workforce_api_requires_authentication(self):
		self.client.force_authenticate(user=None)
		response = self.client.get(reverse('employee-list'))
		self.assertEqual(response.status_code, 401)
