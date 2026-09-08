from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class Role(models.Model):
	role_name = models.CharField(max_length=100)
	role_code = models.CharField(max_length=50, unique=True)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['role_name']

	def __str__(self):
		return self.role_name


class Permission(models.Model):
	permission_name = models.CharField(max_length=100)
	permission_code = models.CharField(max_length=100, unique=True)
	module = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['module', 'permission_name']

	def __str__(self):
		return self.permission_code


class RolePermission(models.Model):
	role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
	permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['role', 'permission'], name='unique_role_permission'),
		]

	def __str__(self):
		return f'{self.role.role_code}: {self.permission.permission_code}'


class UserManager(BaseUserManager):
	@classmethod
	def normalize_email(cls, email):
		return super().normalize_email(email).lower()

	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('An email address is required.')
		user = self.model(email=self.normalize_email(email), **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=150)
	last_name = models.CharField(max_length=150)
	phone = models.CharField(max_length=30, blank=True)
	is_first_login = models.BooleanField(default=False)
	email_verified = models.BooleanField(default=False)
	phone_verified = models.BooleanField(default=False)
	firebase_uid = models.CharField(max_length=128, unique=True, null=True, blank=True)
	role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users', null=True, blank=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	class Meta:
		ordering = ['email']

	def __str__(self):
		return self.email


class EmailVerificationToken(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification_tokens')
	token_hash = models.CharField(max_length=64, unique=True)
	expires_at = models.DateTimeField()
	used_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']
		indexes = [models.Index(fields=['user', 'used_at', 'expires_at'])]

	def is_expired(self):
		return self.expires_at <= timezone.now()


class OTPVerification(models.Model):
	class Purpose(models.TextChoices):
		EMAIL = 'EMAIL_VERIFICATION', 'Email verification'
		MOBILE = 'MOBILE_VERIFICATION', 'Mobile verification'

	class Channel(models.TextChoices):
		EMAIL = 'EMAIL', 'Email'
		SMS = 'SMS', 'SMS'

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_verifications')
	purpose = models.CharField(max_length=30, choices=Purpose.choices)
	channel = models.CharField(max_length=10, choices=Channel.choices)
	target_hash = models.CharField(max_length=64)
	code_hash = models.CharField(max_length=64)
	expires_at = models.DateTimeField()
	attempt_count = models.PositiveSmallIntegerField(default=0)
	max_attempts = models.PositiveSmallIntegerField(default=5)
	is_verified = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	verified_at = models.DateTimeField(null=True, blank=True)
	invalidated_at = models.DateTimeField(null=True, blank=True)
	last_sent_at = models.DateTimeField()

	class Meta:
		ordering = ['-created_at']
		indexes = [
			models.Index(fields=['user', 'purpose', 'is_verified']),
			models.Index(fields=['expires_at']),
		]

	def is_expired(self):
		return self.expires_at <= timezone.now()
