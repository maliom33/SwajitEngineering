from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Q


class Department(models.Model):
	department_id = models.BigAutoField(primary_key=True)
	department_name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['department_name']
		indexes = [models.Index(fields=['is_active', 'department_name'])]
		verbose_name = 'department'
		verbose_name_plural = 'departments'

	def __str__(self):
		return self.department_name


class Designation(models.Model):
	designation_id = models.BigAutoField(primary_key=True)
	designation_name = models.CharField(max_length=100, unique=True)
	department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='designations', null=True, blank=True)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['designation_name']
		indexes = [models.Index(fields=['is_active', 'designation_name'])]
		verbose_name = 'designation'
		verbose_name_plural = 'designations'

	def __str__(self):
		return self.designation_name


class EmployeeCodeSequence(models.Model):
	next_number = models.PositiveIntegerField(default=1)

	class Meta:
		verbose_name = 'employee code sequence'
		verbose_name_plural = 'employee code sequence'


class Employee(models.Model):
	class EmploymentType(models.TextChoices):
		FULL_TIME = 'FULL_TIME', 'Full Time'
		PART_TIME = 'PART_TIME', 'Part Time'
		CONTRACT = 'CONTRACT', 'Contract'
		INTERN = 'INTERN', 'Intern'

	class Status(models.TextChoices):
		ACTIVE = 'ACTIVE', 'Active'
		INACTIVE = 'INACTIVE', 'Inactive'
		ON_LEAVE = 'ON_LEAVE', 'On Leave'
		RESIGNED = 'RESIGNED', 'Resigned'
		TERMINATED = 'TERMINATED', 'Terminated'

	employee_id = models.BigAutoField(primary_key=True)
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='employee_profile',
	)
	employee_code = models.CharField(max_length=50, unique=True)
	first_name = models.CharField(max_length=150)
	last_name = models.CharField(max_length=150)
	email = models.EmailField()
	phone = models.CharField(max_length=30)
	date_of_birth = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=30, blank=True)
	address = models.TextField(blank=True)
	city = models.CharField(max_length=100, blank=True)
	state = models.CharField(max_length=100, blank=True)
	pincode = models.CharField(max_length=20, blank=True)
	department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees')
	designation = models.ForeignKey(Designation, on_delete=models.PROTECT, related_name='employees')
	joining_date = models.DateField()
	employment_type = models.CharField(max_length=20, choices=EmploymentType.choices)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
	base_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	profile_photo = models.FileField(upload_to='employee_profiles/', blank=True)
	activation_token_hash = models.CharField(max_length=128, blank=True)
	activation_expires_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['employee_code']
		indexes = [
			models.Index(fields=['status', 'department']),
			models.Index(fields=['joining_date']),
		]

	def save(self, *args, **kwargs):
		if self._state.adding and not self.employee_code:
			with transaction.atomic():
				sequence = EmployeeCodeSequence.objects.select_for_update().get(pk=1)
				while True:
					candidate = f'EMP{sequence.next_number:03d}'
					sequence.next_number += 1
					if not type(self).objects.filter(employee_code=candidate).exists():
						self.employee_code = candidate
						sequence.save(update_fields=['next_number'])
						break
				super().save(*args, **kwargs)
			return

		super().save(*args, **kwargs)

	def __str__(self):
		return f'{self.employee_code} - {self.first_name} {self.last_name}'

	def profile_complete(self, user=None):
		account = user or self.user
		return bool(
			account
			and not account.is_first_login
			and self.first_name.strip()
			and self.last_name.strip()
			and self.email
			and self.phone.strip()
			and self.department_id
			and self.designation_id
			and self.gender.strip()
			and self.profile_photo
		)


class Attendance(models.Model):
	class AttendanceMethod(models.TextChoices):
		FACE_RECOGNITION = 'FACE_RECOGNITION', 'Face Recognition'
		MANUAL = 'MANUAL', 'Manual'

	class Status(models.TextChoices):
		PRESENT = 'PRESENT', 'Present'
		ABSENT = 'ABSENT', 'Absent'
		HALF_DAY = 'HALF_DAY', 'Half Day'
		LATE = 'LATE', 'Late'
		ON_LEAVE = 'ON_LEAVE', 'On Leave'

	attendance_id = models.BigAutoField(primary_key=True)
	employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='attendance_records')
	attendance_date = models.DateField()
	check_in = models.DateTimeField(null=True, blank=True)
	check_out = models.DateTimeField(null=True, blank=True)
	photo = models.ImageField(upload_to='attendance/%Y/%m/%d/', null=True, blank=True)
	check_out_photo = models.ImageField(upload_to='attendance/check-out/%Y/%m/%d/', null=True, blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, validators=[MinValueValidator(Decimal('-90')), MaxValueValidator(Decimal('90'))])
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, validators=[MinValueValidator(Decimal('-180')), MaxValueValidator(Decimal('180'))])
	check_out_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, validators=[MinValueValidator(Decimal('-90')), MaxValueValidator(Decimal('90'))])
	check_out_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, validators=[MinValueValidator(Decimal('-180')), MaxValueValidator(Decimal('180'))])
	status = models.CharField(max_length=20, choices=Status.choices)
	work_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0'))])
	total_work_minutes = models.PositiveIntegerField(null=True, blank=True)
	attendance_method = models.CharField(max_length=20, choices=AttendanceMethod.choices, default=AttendanceMethod.MANUAL)
	confidence_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))])
	remarks = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-attendance_date', 'employee']
		constraints = [
			models.UniqueConstraint(fields=['employee', 'attendance_date'], name='unique_employee_attendance_date'),
		]
		indexes = [models.Index(fields=['attendance_date', 'status'])]

	def __str__(self):
		return f'{self.employee.employee_code} - {self.attendance_date}'

	def clean(self):
		if self.check_in and self.check_out and self.check_out < self.check_in:
			raise ValidationError({'check_out': 'Check-out cannot be before check-in.'})
		if self.attendance_method == self.AttendanceMethod.MANUAL and self.confidence_score is not None:
			raise ValidationError({'confidence_score': 'Manual attendance cannot have a confidence score.'})


class EmployeeFaceData(models.Model):
	face_data_id = models.BigAutoField(primary_key=True)
	employee = models.OneToOneField(Employee, on_delete=models.PROTECT, related_name='face_data')
	secure_reference = models.CharField(max_length=500)
	face_encoding_reference = models.CharField(max_length=500, blank=True)
	model_version = models.CharField(max_length=100, blank=True)
	registered_at = models.DateTimeField()
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['employee']

	def __str__(self):
		return f'Face data for {self.employee.employee_code}'


class LeaveType(models.Model):
	leave_type_id = models.BigAutoField(primary_key=True)
	leave_name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)
	maximum_days = models.PositiveIntegerField()
	is_paid = models.BooleanField(default=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['leave_name']

	def __str__(self):
		return self.leave_name


class LeaveRequest(models.Model):
	class Status(models.TextChoices):
		PENDING = 'PENDING', 'Pending'
		APPROVED = 'APPROVED', 'Approved'
		REJECTED = 'REJECTED', 'Rejected'
		CANCELLED = 'CANCELLED', 'Cancelled'

	leave_request_id = models.BigAutoField(primary_key=True)
	employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='leave_requests')
	leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT, related_name='leave_requests')
	start_date = models.DateField()
	end_date = models.DateField()
	total_days = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.5'))])
	reason = models.TextField()
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='approved_leave_requests')
	approved_at = models.DateTimeField(null=True, blank=True)
	rejection_reason = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
		indexes = [models.Index(fields=['employee', 'status']), models.Index(fields=['start_date', 'end_date'])]

	def __str__(self):
		return f'{self.employee.employee_code} leave {self.start_date} to {self.end_date}'

	def clean(self):
		if self.end_date < self.start_date:
			raise ValidationError({'end_date': 'End date cannot be before start date.'})


class SalaryStructure(models.Model):
	salary_structure_id = models.BigAutoField(primary_key=True)
	employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='salary_structures')
	effective_from = models.DateField()
	effective_to = models.DateField(null=True, blank=True)
	basic_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	hra = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	transport_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	other_allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	provident_fund = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	professional_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	other_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-effective_from']
		indexes = [models.Index(fields=['employee', '-effective_from'])]

	def __str__(self):
		return f'{self.employee.employee_code} salary from {self.effective_from}'

	def clean(self):
		if self.effective_to and self.effective_to < self.effective_from:
			raise ValidationError({'effective_to': 'Effective-to cannot be before effective-from.'})
		existing_periods = SalaryStructure.objects.filter(employee=self.employee).exclude(pk=self.pk)
		if self.effective_to:
			overlap = existing_periods.filter(
				effective_from__lte=self.effective_to,
			).filter(Q(effective_to__isnull=True) | Q(effective_to__gte=self.effective_from))
		else:
			overlap = existing_periods.filter(
				Q(effective_to__isnull=True) | Q(effective_to__gte=self.effective_from),
			)
		if overlap.exists():
			raise ValidationError('Salary periods cannot overlap.')


class PayrollRun(models.Model):
	class Status(models.TextChoices):
		DRAFT = 'DRAFT', 'Draft'
		PROCESSING = 'PROCESSING', 'Processing'
		COMPLETED = 'COMPLETED', 'Completed'
		CANCELLED = 'CANCELLED', 'Cancelled'

	payroll_run_id = models.BigAutoField(primary_key=True)
	period_start = models.DateField()
	period_end = models.DateField()
	processed_date = models.DateTimeField(null=True, blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
	processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='processed_payroll_runs')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-period_start']
		constraints = [models.UniqueConstraint(fields=['period_start', 'period_end'], name='unique_payroll_period')]

	def __str__(self):
		return f'Payroll {self.period_start} to {self.period_end}'

	def clean(self):
		if self.period_end < self.period_start:
			raise ValidationError({'period_end': 'Period end cannot be before period start.'})


class PayrollItem(models.Model):
	class PaymentStatus(models.TextChoices):
		PENDING = 'PENDING', 'Pending'
		PAID = 'PAID', 'Paid'
		FAILED = 'FAILED', 'Failed'
		CANCELLED = 'CANCELLED', 'Cancelled'

	payroll_item_id = models.BigAutoField(primary_key=True)
	payroll_run = models.ForeignKey(PayrollRun, on_delete=models.PROTECT, related_name='items')
	employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='payroll_items')
	basic_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	overtime = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	gross_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	net_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
	payment_date = models.DateField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['payroll_run', 'employee']
		constraints = [models.UniqueConstraint(fields=['payroll_run', 'employee'], name='unique_payroll_employee')]

	def __str__(self):
		return f'{self.payroll_run} - {self.employee.employee_code}'


class EmployeePerformance(models.Model):
	performance_id = models.BigAutoField(primary_key=True)
	employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='performance_reviews')
	evaluation_period_start = models.DateField()
	evaluation_period_end = models.DateField()
	attendance_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))])
	task_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))])
	delivery_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))])
	overall_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))])
	remarks = models.TextField(blank=True)
	evaluated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='evaluated_performances')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-evaluation_period_end']

	def __str__(self):
		return f'{self.employee.employee_code} performance {self.evaluation_period_end}'

	def clean(self):
		if self.evaluation_period_end < self.evaluation_period_start:
			raise ValidationError({'evaluation_period_end': 'Evaluation end cannot be before start.'})


class EmployeeDocument(models.Model):
	class DocumentType(models.TextChoices):
		ID_PROOF = 'ID_PROOF', 'ID Proof'
		JOINING_LETTER = 'JOINING_LETTER', 'Joining Letter'
		EXPERIENCE_LETTER = 'EXPERIENCE_LETTER', 'Experience Letter'
		CERTIFICATE = 'CERTIFICATE', 'Certificate'
		CONTRACT = 'CONTRACT', 'Contract'
		OTHER = 'OTHER', 'Other'

	document_id = models.BigAutoField(primary_key=True)
	employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='documents')
	document_type = models.CharField(max_length=30, choices=DocumentType.choices)
	document_name = models.CharField(max_length=255)
	file_path = models.FileField(upload_to='employee_documents/')
	uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='uploaded_employee_documents')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	expiry_date = models.DateField(null=True, blank=True)
	is_verified = models.BooleanField(default=False)
	verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='verified_employee_documents')
	verified_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		ordering = ['-uploaded_at']
		indexes = [models.Index(fields=['employee', 'document_type'])]

	def __str__(self):
		return f'{self.employee.employee_code} - {self.document_name}'
