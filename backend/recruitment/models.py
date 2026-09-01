import os
import uuid
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q

from workforce.models import Department, Designation, Employee


def resume_upload_path(instance, filename):
	extension = os.path.splitext(filename)[1].lower()
	return f'recruitment/resumes/{instance.candidate.candidate_code}/{uuid.uuid4().hex}{extension}'


class JobPosition(models.Model):
	class Status(models.TextChoices):
		DRAFT = 'DRAFT', 'Draft'
		OPEN = 'OPEN', 'Open'
		ON_HOLD = 'ON_HOLD', 'On Hold'
		CLOSED = 'CLOSED', 'Closed'
		CANCELLED = 'CANCELLED', 'Cancelled'

	job_id = models.BigAutoField(primary_key=True)
	job_code = models.CharField(max_length=50, unique=True)
	job_title = models.CharField(max_length=150)
	department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='job_positions')
	designation = models.ForeignKey(Designation, on_delete=models.PROTECT, related_name='job_positions')
	description = models.TextField()
	required_skills = models.JSONField(default=list)
	minimum_experience = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	minimum_qualification = models.CharField(max_length=150)
	salary_range_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0'))])
	salary_range_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0'))])
	number_of_openings = models.PositiveIntegerField(default=1)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_job_positions')
	opening_date = models.DateField()
	closing_date = models.DateField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-opening_date', 'job_title']
		indexes = [models.Index(fields=['status', 'opening_date']), models.Index(fields=['job_code'])]

	def __str__(self):
		return f'{self.job_code} - {self.job_title}'

	def clean(self):
		if self.salary_range_min is not None and self.salary_range_max is not None and self.salary_range_max < self.salary_range_min:
			raise ValidationError({'salary_range_max': 'Maximum salary cannot be lower than minimum salary.'})
		if self.closing_date and self.closing_date < self.opening_date:
			raise ValidationError({'closing_date': 'Closing date cannot be before opening date.'})


class Candidate(models.Model):
	class Status(models.TextChoices):
		NEW = 'NEW', 'New'
		SCREENING = 'SCREENING', 'Screening'
		SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
		INTERVIEW = 'INTERVIEW', 'Interview'
		SELECTED = 'SELECTED', 'Selected'
		REJECTED = 'REJECTED', 'Rejected'
		WITHDRAWN = 'WITHDRAWN', 'Withdrawn'

	candidate_id = models.BigAutoField(primary_key=True)
	employee = models.OneToOneField(Employee, on_delete=models.PROTECT, null=True, blank=True, related_name='source_candidate')
	candidate_code = models.CharField(max_length=50, unique=True)
	first_name = models.CharField(max_length=150)
	last_name = models.CharField(max_length=150)
	email = models.EmailField(db_index=True)
	phone = models.CharField(max_length=30)
	address = models.TextField(blank=True)
	city = models.CharField(max_length=100, blank=True)
	state = models.CharField(max_length=100, blank=True)
	pincode = models.CharField(max_length=20, blank=True)
	date_of_birth = models.DateField(null=True, blank=True)
	highest_qualification = models.CharField(max_length=150)
	total_experience_years = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	current_company = models.CharField(max_length=150, blank=True)
	current_designation = models.CharField(max_length=150, blank=True)
	notice_period_days = models.PositiveIntegerField(default=0)
	candidate_status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
		indexes = [models.Index(fields=['candidate_status', 'created_at'])]

	def __str__(self):
		return f'{self.candidate_code} - {self.first_name} {self.last_name}'


class CandidateResume(models.Model):
	class ParsingStatus(models.TextChoices):
		PENDING = 'PENDING', 'Pending'
		COMPLETED = 'COMPLETED', 'Completed'
		FAILED = 'FAILED', 'Failed'

	resume_id = models.BigAutoField(primary_key=True)
	candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT, related_name='resumes')
	file = models.FileField(upload_to=resume_upload_path, validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])
	original_filename = models.CharField(max_length=255)
	file_type = models.CharField(max_length=100)
	file_size = models.PositiveBigIntegerField()
	uploaded_at = models.DateTimeField(auto_now_add=True)
	parsed_text = models.TextField(blank=True)
	parsing_status = models.CharField(max_length=20, choices=ParsingStatus.choices, default=ParsingStatus.PENDING)
	is_primary = models.BooleanField(default=False)

	class Meta:
		ordering = ['-uploaded_at']
		constraints = [models.UniqueConstraint(fields=['candidate'], condition=Q(is_primary=True), name='one_primary_resume_per_candidate')]

	def __str__(self):
		return f'{self.candidate.candidate_code} - {self.original_filename}'

	def clean(self):
		max_size = 10 * 1024 * 1024
		if self.file_size > max_size:
			raise ValidationError({'file': 'Resume files must be 10 MB or smaller.'})


class CandidateSkill(models.Model):
	class Source(models.TextChoices):
		MANUAL = 'MANUAL', 'Manual'
		RESUME_PARSER = 'RESUME_PARSER', 'Resume Parser'
		AI_SCREENING = 'AI_SCREENING', 'AI Screening'

	candidate_skill_id = models.BigAutoField(primary_key=True)
	candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT, related_name='skills')
	skill_name = models.CharField(max_length=100)
	proficiency_level = models.CharField(max_length=50, blank=True)
	years_of_experience = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	source = models.CharField(max_length=20, choices=Source.choices, default=Source.MANUAL)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['skill_name']
		constraints = [models.UniqueConstraint(fields=['candidate', 'skill_name'], name='unique_candidate_skill')]

	def __str__(self):
		return f'{self.candidate.candidate_code} - {self.skill_name}'


class JobApplication(models.Model):
	class Status(models.TextChoices):
		APPLIED = 'APPLIED', 'Applied'
		UNDER_SCREENING = 'UNDER_SCREENING', 'Under Screening'
		SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
		INTERVIEW_SCHEDULED = 'INTERVIEW_SCHEDULED', 'Interview Scheduled'
		INTERVIEWED = 'INTERVIEWED', 'Interviewed'
		SELECTED = 'SELECTED', 'Selected'
		REJECTED = 'REJECTED', 'Rejected'
		WITHDRAWN = 'WITHDRAWN', 'Withdrawn'

	application_id = models.BigAutoField(primary_key=True)
	application_number = models.CharField(max_length=50, unique=True)
	candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT, related_name='applications')
	job = models.ForeignKey(JobPosition, on_delete=models.PROTECT, related_name='applications')
	resume = models.ForeignKey(CandidateResume, on_delete=models.PROTECT, related_name='applications')
	application_date = models.DateField(auto_now_add=True)
	application_status = models.CharField(max_length=30, choices=Status.choices, default=Status.APPLIED)
	screening_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))])
	recruiter_notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-application_date']
		constraints = [models.UniqueConstraint(fields=['candidate', 'job'], condition=~Q(application_status__in=['REJECTED', 'WITHDRAWN']), name='one_active_application_per_job')]
		indexes = [models.Index(fields=['application_status', 'application_date'])]

	def __str__(self):
		return self.application_number

	def clean(self):
		if self.resume_id and self.resume.candidate_id != self.candidate_id:
			raise ValidationError({'resume': 'Resume must belong to the selected candidate.'})


class RecruitmentScreening(models.Model):
	class Recommendation(models.TextChoices):
		RECOMMENDED = 'RECOMMENDED', 'Recommended'
		CONSIDER = 'CONSIDER', 'Consider'
		NOT_RECOMMENDED = 'NOT_RECOMMENDED', 'Not Recommended'

	screening_id = models.BigAutoField(primary_key=True)
	application = models.ForeignKey(JobApplication, on_delete=models.PROTECT, related_name='screenings')
	model_version = models.CharField(max_length=100)
	skills_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))])
	education_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))])
	experience_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))])
	overall_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))])
	matched_skills = models.JSONField(default=list)
	missing_skills = models.JSONField(default=list)
	recommendation = models.CharField(max_length=20, choices=Recommendation.choices)
	explanation = models.TextField(blank=True)
	screened_at = models.DateTimeField()
	screened_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='recruitment_screenings')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-screened_at']

	def __str__(self):
		return f'{self.application.application_number} - {self.overall_score}'


class Interview(models.Model):
	class InterviewType(models.TextChoices):
		ONLINE = 'ONLINE', 'Online'
		OFFLINE = 'OFFLINE', 'Offline'
		PHONE = 'PHONE', 'Phone'

	class Status(models.TextChoices):
		SCHEDULED = 'SCHEDULED', 'Scheduled'
		COMPLETED = 'COMPLETED', 'Completed'
		CANCELLED = 'CANCELLED', 'Cancelled'
		RESCHEDULED = 'RESCHEDULED', 'Rescheduled'
		NO_SHOW = 'NO_SHOW', 'No Show'

	interview_id = models.BigAutoField(primary_key=True)
	application = models.ForeignKey(JobApplication, on_delete=models.PROTECT, related_name='interviews')
	interview_round = models.PositiveIntegerField(default=1)
	interview_type = models.CharField(max_length=20, choices=InterviewType.choices)
	scheduled_at = models.DateTimeField()
	duration_minutes = models.PositiveIntegerField(default=30)
	interviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='recruitment_interviews')
	location = models.CharField(max_length=255, blank=True)
	meeting_link = models.URLField(blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
	score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))])
	feedback = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-scheduled_at']
		constraints = [models.UniqueConstraint(fields=['application', 'interview_round'], name='unique_interview_round')]

	def __str__(self):
		return f'{self.application.application_number} - Round {self.interview_round}'
