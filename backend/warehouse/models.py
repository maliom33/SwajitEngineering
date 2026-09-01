from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q

from workforce.models import Employee


class Warehouse(models.Model):
	class Status(models.TextChoices):
		ACTIVE = 'ACTIVE', 'Active'
		INACTIVE = 'INACTIVE', 'Inactive'
		UNDER_MAINTENANCE = 'UNDER_MAINTENANCE', 'Under Maintenance'

	warehouse_id = models.BigAutoField(primary_key=True)
	warehouse_code = models.CharField(max_length=50, unique=True)
	warehouse_name = models.CharField(max_length=150)
	location = models.CharField(max_length=150)
	address = models.TextField()
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	pincode = models.CharField(max_length=20)
	contact_number = models.CharField(max_length=30)
	manager = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='managed_warehouses')
	status = models.CharField(max_length=25, choices=Status.choices, default=Status.ACTIVE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['warehouse_name']
		indexes = [models.Index(fields=['status', 'warehouse_name'])]

	def __str__(self):
		return f'{self.warehouse_code} - {self.warehouse_name}'


class ProductCategory(models.Model):
	category_id = models.BigAutoField(primary_key=True)
	category_code = models.CharField(max_length=50, unique=True)
	category_name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['category_name']

	def __str__(self):
		return self.category_name


class Product(models.Model):
	class Unit(models.TextChoices):
		PCS = 'PCS', 'Pieces'
		KG = 'KG', 'Kilogram'
		GRAM = 'GRAM', 'Gram'
		LITRE = 'LITRE', 'Litre'
		METER = 'METER', 'Meter'
		BOX = 'BOX', 'Box'
		PACK = 'PACK', 'Pack'
		OTHER = 'OTHER', 'Other'

	class Status(models.TextChoices):
		ACTIVE = 'ACTIVE', 'Active'
		INACTIVE = 'INACTIVE', 'Inactive'
		DISCONTINUED = 'DISCONTINUED', 'Discontinued'

	product_id = models.BigAutoField(primary_key=True)
	sku = models.CharField(max_length=100, unique=True)
	product_code = models.CharField(max_length=100, unique=True)
	product_name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products')
	unit = models.CharField(max_length=20, choices=Unit.choices, default=Unit.PCS)
	unit_price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	reorder_level = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	reorder_quantity = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	weight = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True, validators=[MinValueValidator(Decimal('0'))])
	dimensions = models.CharField(max_length=150, blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['product_name']
		indexes = [models.Index(fields=['product_name']), models.Index(fields=['status', 'category'])]

	def __str__(self):
		return f'{self.sku} - {self.product_name}'


class Supplier(models.Model):
	class Status(models.TextChoices):
		ACTIVE = 'ACTIVE', 'Active'
		INACTIVE = 'INACTIVE', 'Inactive'
		BLOCKED = 'BLOCKED', 'Blocked'

	supplier_id = models.BigAutoField(primary_key=True)
	supplier_code = models.CharField(max_length=50, unique=True)
	supplier_name = models.CharField(max_length=200)
	contact_person = models.CharField(max_length=150)
	email = models.EmailField()
	phone = models.CharField(max_length=30)
	alternate_phone = models.CharField(max_length=30, blank=True)
	address = models.TextField()
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	pincode = models.CharField(max_length=20)
	tax_identifier = models.CharField(max_length=100, blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['supplier_name']
		indexes = [models.Index(fields=['supplier_name']), models.Index(fields=['email']), models.Index(fields=['status'])]

	def __str__(self):
		return f'{self.supplier_code} - {self.supplier_name}'


class Inventory(models.Model):
	inventory_id = models.BigAutoField(primary_key=True)
	warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='inventory')
	product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='inventory')
	quantity_available = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	quantity_reserved = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	quantity_damaged = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	reorder_level = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	last_stock_update = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['warehouse', 'product']
		constraints = [
			models.UniqueConstraint(fields=['warehouse', 'product'], name='unique_warehouse_product_inventory'),
			models.CheckConstraint(condition=Q(quantity_available__gte=0), name='inventory_available_nonnegative'),
			models.CheckConstraint(condition=Q(quantity_reserved__gte=0), name='inventory_reserved_nonnegative'),
			models.CheckConstraint(condition=Q(quantity_damaged__gte=0), name='inventory_damaged_nonnegative'),
			models.CheckConstraint(condition=Q(quantity_reserved__lte=F('quantity_available')), name='inventory_reserved_lte_available'),
		]
		indexes = [models.Index(fields=['warehouse', 'product']), models.Index(fields=['quantity_available', 'reorder_level'])]

	@property
	def available_quantity(self):
		return self.quantity_available - self.quantity_reserved

	def __str__(self):
		return f'{self.warehouse.warehouse_code} - {self.product.sku}'


class StockTransaction(models.Model):
	class TransactionType(models.TextChoices):
		PURCHASE = 'PURCHASE', 'Purchase'
		SALE = 'SALE', 'Sale'
		ORDER_ALLOCATION = 'ORDER_ALLOCATION', 'Order Allocation'
		ORDER_RELEASE = 'ORDER_RELEASE', 'Order Release'
		RETURN = 'RETURN', 'Return'
		DAMAGE = 'DAMAGE', 'Damage'
		ADJUSTMENT = 'ADJUSTMENT', 'Adjustment'
		TRANSFER_IN = 'TRANSFER_IN', 'Transfer In'
		TRANSFER_OUT = 'TRANSFER_OUT', 'Transfer Out'

	transaction_id = models.BigAutoField(primary_key=True)
	warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='stock_transactions')
	product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stock_transactions')
	transaction_type = models.CharField(max_length=30, choices=TransactionType.choices)
	quantity = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	reference_type = models.CharField(max_length=50, blank=True)
	reference_id = models.CharField(max_length=100, blank=True)
	balance_after = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='stock_transactions')
	transaction_date = models.DateTimeField(auto_now_add=True)
	remarks = models.TextField(blank=True)

	class Meta:
		ordering = ['-transaction_date']
		indexes = [models.Index(fields=['warehouse', 'product', 'transaction_date']), models.Index(fields=['transaction_type', 'transaction_date'])]

	def __str__(self):
		return f'{self.transaction_type} - {self.product.sku} - {self.quantity}'


class PurchaseOrder(models.Model):
	class Status(models.TextChoices):
		DRAFT = 'DRAFT', 'Draft'
		PENDING_APPROVAL = 'PENDING_APPROVAL', 'Pending Approval'
		APPROVED = 'APPROVED', 'Approved'
		ORDERED = 'ORDERED', 'Ordered'
		PARTIALLY_RECEIVED = 'PARTIALLY_RECEIVED', 'Partially Received'
		RECEIVED = 'RECEIVED', 'Received'
		CANCELLED = 'CANCELLED', 'Cancelled'
		CLOSED = 'CLOSED', 'Closed'

	purchase_order_id = models.BigAutoField(primary_key=True)
	purchase_order_number = models.CharField(max_length=50, unique=True)
	supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
	warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='purchase_orders')
	order_date = models.DateField()
	expected_delivery_date = models.DateField(null=True, blank=True)
	subtotal = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	tax_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	discount_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	total_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_purchase_orders')
	approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='approved_purchase_orders')
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-order_date']

	def __str__(self):
		return self.purchase_order_number

	def clean(self):
		if self.expected_delivery_date and self.expected_delivery_date < self.order_date:
			raise ValidationError({'expected_delivery_date': 'Expected delivery cannot be before order date.'})
		if self.total_amount != self.subtotal + self.tax_amount - self.discount_amount:
			raise ValidationError({'total_amount': 'Total must equal subtotal plus tax minus discount.'})


class PurchaseOrderItem(models.Model):
	purchase_order_item_id = models.BigAutoField(primary_key=True)
	purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='purchase_order_items')
	quantity_ordered = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	quantity_received = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	unit_price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	discount_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
	line_total = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['purchase_order', 'purchase_order_item_id']

	def __str__(self):
		return f'{self.purchase_order.purchase_order_number} - {self.product.sku}'

	def clean(self):
		if self.quantity_received > self.quantity_ordered:
			raise ValidationError({'quantity_received': 'Received quantity cannot exceed ordered quantity.'})


class StockTransfer(models.Model):
	class Status(models.TextChoices):
		DRAFT = 'DRAFT', 'Draft'
		REQUESTED = 'REQUESTED', 'Requested'
		APPROVED = 'APPROVED', 'Approved'
		IN_TRANSIT = 'IN_TRANSIT', 'In Transit'
		RECEIVED = 'RECEIVED', 'Received'
		CANCELLED = 'CANCELLED', 'Cancelled'

	transfer_id = models.BigAutoField(primary_key=True)
	transfer_number = models.CharField(max_length=50, unique=True)
	source_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='outgoing_transfers')
	destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='incoming_transfers')
	transfer_date = models.DateField()
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
	initiated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='initiated_stock_transfers')
	approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='approved_stock_transfers')
	received_at = models.DateTimeField(null=True, blank=True)
	remarks = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-transfer_date']

	def __str__(self):
		return self.transfer_number

	def clean(self):
		if self.source_warehouse_id == self.destination_warehouse_id:
			raise ValidationError({'destination_warehouse': 'Source and destination warehouses must differ.'})


class StockTransferItem(models.Model):
	transfer_item_id = models.BigAutoField(primary_key=True)
	transfer = models.ForeignKey(StockTransfer, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stock_transfer_items')
	quantity = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	received_quantity = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])

	class Meta:
		constraints = [models.CheckConstraint(condition=Q(received_quantity__lte=F('quantity')), name='transfer_received_lte_quantity')]

	def __str__(self):
		return f'{self.transfer.transfer_number} - {self.product.sku}'

	def clean(self):
		if self.received_quantity > self.quantity:
			raise ValidationError({'received_quantity': 'Received quantity cannot exceed transfer quantity.'})


class StockReservation(models.Model):
	class Status(models.TextChoices):
		RESERVED = 'RESERVED', 'Reserved'
		ALLOCATED = 'ALLOCATED', 'Allocated'
		RELEASED = 'RELEASED', 'Released'

	reservation_id = models.BigAutoField(primary_key=True)
	order = models.OneToOneField('sales.Order', on_delete=models.PROTECT, related_name='stock_reservation')
	warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='stock_reservations')
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.RESERVED)
	reserved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='stock_reservations')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.order.order_number} - {self.status}'


class StockReservationItem(models.Model):
	reservation_item_id = models.BigAutoField(primary_key=True)
	reservation = models.ForeignKey(StockReservation, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stock_reservation_items')
	quantity = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

	class Meta:
		constraints = [models.UniqueConstraint(fields=['reservation', 'product'], name='unique_reserved_order_product')]

	def __str__(self):
		return f'{self.reservation} - {self.product.sku}'
