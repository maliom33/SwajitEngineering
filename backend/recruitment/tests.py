from datetime import date, datetime, timezone
from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import Permission, Role, RolePermission, User
from workforce.models import Department, Designation

from .models import Candidate, CandidateResume, CandidateSkill, Interview, JobApplication, JobPosition, RecruitmentScreening
from .services.conversion import convert_selected_candidate_to_employee


class RecruitmentTests(APITestCase):
	def setUp(self):
		self.role = Role.objects.create(role_name='HR Manager', role_code='HR_MANAGER')
		self.permission = Permission.objects.get(permission_code='MANAGE_JOB_POSITIONS')
		RolePermission.objects.create(role=self.role, permission=self.permission)
		self.user = User.objects.create_user(email='hr@example.com', password='SecurePassword123!', first_name='HR', last_name='Manager', role=self.role)
		self.department = Department.objects.create(department_name='Recruitment')
		self.designation = Designation.objects.create(designation_name='Engineer')
		self.job = JobPosition.objects.create(
			job_code='JOB-001', job_title='Backend Engineer', department=self.department,
			designation=self.designation, description='Build APIs', required_skills=['Python'],
			minimum_experience=Decimal('2'), minimum_qualification='B.Tech', number_of_openings=1,
			created_by=self.user, opening_date=date(2026, 8, 1),
		)
		self.candidate = Candidate.objects.create(
			candidate_code='CAN-001', first_name='Ravi', last_name='Kumar', email='ravi@example.com',
			phone='1234567890', highest_qualification='B.Tech', total_experience_years=Decimal('3'),
		)
		self.resume = CandidateResume.objects.create(
			candidate=self.candidate,
			file=SimpleUploadedFile('resume.pdf', b'%PDF-test', content_type='application/pdf'),
			original_filename='resume.pdf', file_type='application/pdf', file_size=9,
		)

	def test_job_position_creation_and_duplicate_code_rejection(self):
		self.assertEqual(self.job.job_code, 'JOB-001')
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				JobPosition.objects.create(
					job_code='JOB-001', job_title='Duplicate', department=self.department,
					designation=self.designation, description='Duplicate', minimum_qualification='B.Tech',
					created_by=self.user, opening_date=date(2026, 8, 2),
				)

	def test_candidate_creation_and_duplicate_code_rejection(self):
		self.assertEqual(self.candidate.candidate_status, Candidate.Status.NEW)
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Candidate.objects.create(
					candidate_code='CAN-001', first_name='Duplicate', last_name='Candidate',
					email='duplicate@example.com', phone='0000000000', highest_qualification='B.Tech',
				)

	def test_resume_upload_validation(self):
		invalid = CandidateResume(
			candidate=self.candidate,
			file_size=11 * 1024 * 1024,
			original_filename='large.pdf',
			file_type='application/pdf',
		)
		with self.assertRaises(ValidationError):
			invalid.full_clean()

	def test_candidate_skill_and_application_creation(self):
		skill = CandidateSkill.objects.create(candidate=self.candidate, skill_name='Python')
		application = JobApplication.objects.create(application_number='APP-001', candidate=self.candidate, job=self.job, resume=self.resume)
		self.assertEqual(skill.skill_name, 'Python')
		self.assertEqual(application.application_status, JobApplication.Status.APPLIED)

	def test_duplicate_active_application_is_rejected(self):
		JobApplication.objects.create(application_number='APP-001', candidate=self.candidate, job=self.job, resume=self.resume)
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				JobApplication.objects.create(application_number='APP-002', candidate=self.candidate, job=self.job, resume=self.resume)

	def test_screening_score_validation(self):
		application = JobApplication.objects.create(application_number='APP-001', candidate=self.candidate, job=self.job, resume=self.resume)
		screening = RecruitmentScreening(
			application=application, model_version='pending', skills_score=Decimal('101'), education_score=Decimal('80'),
			experience_score=Decimal('80'), overall_score=Decimal('80'), recommendation='CONSIDER',
			screened_at=datetime.now(timezone.utc),
		)
		with self.assertRaises(ValidationError):
			screening.full_clean()

	def test_interview_creation_and_status(self):
		application = JobApplication.objects.create(application_number='APP-001', candidate=self.candidate, job=self.job, resume=self.resume)
		interview = Interview.objects.create(
			application=application, interview_round=1, interview_type=Interview.InterviewType.ONLINE,
			scheduled_at=datetime.now(timezone.utc), interviewer=self.user, status=Interview.Status.SCHEDULED,
		)
		self.assertEqual(interview.status, Interview.Status.SCHEDULED)

	def test_selected_candidate_converts_to_existing_employee_once(self):
		application = JobApplication.objects.create(application_number='APP-001', candidate=self.candidate, job=self.job, resume=self.resume, application_status=JobApplication.Status.SELECTED)
		employee = convert_selected_candidate_to_employee(
			self.candidate, department=self.department, designation=self.designation,
			joining_date=date(2026, 9, 1), employment_type='FULL_TIME', base_salary=Decimal('60000'),
		)
		self.candidate.refresh_from_db()
		self.assertEqual(self.candidate.employee_id, employee.employee_id)
		self.assertEqual(convert_selected_candidate_to_employee(
			self.candidate, department=self.department, designation=self.designation,
			joining_date=date(2026, 9, 1), employment_type='FULL_TIME', base_salary=Decimal('60000'),
		).employee_id, employee.employee_id)

	def test_recruitment_api_requires_authentication(self):
		self.client.force_authenticate(user=None)
		response = self.client.get(reverse('recruitment-candidate-list'))
		self.assertEqual(response.status_code, 401)

	def test_recruitment_write_uses_rbac_permission(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.post(reverse('recruitment-job-list'), {
			'job_code': 'JOB-002', 'job_title': 'QA Engineer', 'department': self.department.pk,
			'designation': self.designation.pk, 'description': 'Test APIs', 'minimum_qualification': 'B.Tech',
			'opening_date': '2026-08-20',
		}, format='json')
		self.assertEqual(response.status_code, 201)

# Create your tests here.
