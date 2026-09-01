from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models

from logistics.models import Delivery
from sales.models import Order
from warehouse.models import Product, Warehouse


class Dispatch(models.Model):
	class Status(models.TextChoices):
		SCHEDULED = 'SCHEDULED', 'Scheduled'
		PREPARING = 'PREPARING', 'Preparing'
		READY = 'READY', 'Ready'
		HANDED_OVER = 'HANDED_OVER', 'Handed Over'
		DISPATCHED = 'DISPATCHED', 'Dispatched'
		CANCELLED = 'CANCELLED', 'Cancelled'
		ON_HOLD = 'ON_HOLD', 'On Hold'

	dispatch_id = models.BigAutoField(primary_key=True)
	dispatch_number = models.CharField(max_length=50, unique=True)
	order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='dispatches')
	delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT, related_name='dispatches')
	warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='dispatches')
	scheduled_dispatch_date = models.DateField()
	actual_dispatch_date = models.DateTimeField(null=True, blank=True)
	prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='prepared_dispatches')
	handed_over_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='handed_over_dispatches')
	dispatch_status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
	remarks = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-scheduled_dispatch_date']
		constraints = [models.UniqueConstraint(fields=['order'], condition=~models.Q(dispatch_status__in=['CANCELLED']), name='one_active_dispatch_per_order')]
		indexes = [models.Index(fields=['dispatch_status', 'scheduled_dispatch_date']), models.Index(fields=['order']), models.Index(fields=['delivery'])]

	def __str__(self):
		return self.dispatch_number


class DispatchItem(models.Model):
	dispatch_item_id = models.BigAutoField(primary_key=True)
	dispatch = models.ForeignKey(Dispatch, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='dispatch_items')
	quantity = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	package_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
	remarks = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		constraints = [models.UniqueConstraint(fields=['dispatch', 'product'], name='unique_dispatch_product')]

	def __str__(self):
		return f'{self.dispatch.dispatch_number} - {self.product.sku}'


class DeliveryChallan(models.Model):
	class Status(models.TextChoices):
		DRAFT = 'DRAFT', 'Draft'
		GENERATED = 'GENERATED', 'Generated'
		ISSUED = 'ISSUED', 'Issued'
		ACKNOWLEDGED = 'ACKNOWLEDGED', 'Acknowledged'
		CANCELLED = 'CANCELLED', 'Cancelled'

	challan_id = models.BigAutoField(primary_key=True)
	challan_number = models.CharField(max_length=50, unique=True)
	dispatch = models.OneToOneField(Dispatch, on_delete=models.PROTECT, related_name='challan')
	challan_date = models.DateField()
	issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='issued_challans')
	received_by = models.CharField(max_length=150, blank=True)
	vehicle_number_snapshot = models.CharField(max_length=50)
	driver_name_snapshot = models.CharField(max_length=200)
	delivery_address = models.TextField()
	total_items = models.PositiveIntegerField(default=0)
	total_quantity = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.GENERATED)
	remarks = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.challan_number


class DispatchStatusHistory(models.Model):
	history_id = models.BigAutoField(primary_key=True)
	dispatch = models.ForeignKey(Dispatch, on_delete=models.PROTECT, related_name='status_history')
	previous_status = models.CharField(max_length=20, blank=True)
	new_status = models.CharField(max_length=20, choices=Dispatch.Status.choices)
	changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='dispatch_status_changes')
	remarks = models.TextField(blank=True)
	changed_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-changed_at']

	def __str__(self):
		return f'{self.dispatch.dispatch_number}: {self.previous_status} -> {self.new_status}'


class DispatchDocument(models.Model):
	class DocumentType(models.TextChoices):
		DELIVERY_CHALLAN = 'DELIVERY_CHALLAN', 'Delivery Challan'
		PACKING_LIST = 'PACKING_LIST', 'Packing List'
		OTHER = 'OTHER', 'Other'

	document_id = models.BigAutoField(primary_key=True)
	dispatch = models.ForeignKey(Dispatch, on_delete=models.PROTECT, related_name='documents')
	document_type = models.CharField(max_length=30, choices=DocumentType.choices)
	file = models.FileField(upload_to='dispatch/documents/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])])
	original_filename = models.CharField(max_length=255)
	uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='dispatch_documents')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	remarks = models.TextField(blank=True)

	def __str__(self):
		return f'{self.dispatch.dispatch_number} - {self.document_type}'
