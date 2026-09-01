from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import Permission, Role, RolePermission, User
from sales.models import Customer, Order, OrderItem
from workforce.models import Department, Designation, Employee

from .models import Inventory, Product, ProductCategory, PurchaseOrder, PurchaseOrderItem, StockTransaction, StockTransfer, StockTransferItem, Supplier, Warehouse
from .services.inventory import adjust_inventory, allocate_stock_for_order, low_stock_inventory, receive_purchase_order, receive_stock_transfer, release_reserved_stock, reserve_stock_for_order, transfer_stock


WAREHOUSE_PERMISSIONS = [
	'MANAGE_WAREHOUSES', 'MANAGE_PRODUCTS', 'MANAGE_SUPPLIERS', 'VIEW_INVENTORY',
	'MANAGE_INVENTORY', 'MANAGE_PURCHASE_ORDERS', 'MANAGE_STOCK_TRANSFERS',
	'ADJUST_INVENTORY', 'RECEIVE_STOCK', 'ALLOCATE_STOCK',
]


class WarehouseTests(APITestCase):
	def setUp(self):
		self.role = Role.objects.create(role_name='Warehouse Manager', role_code='WAREHOUSE_MANAGER')
		for code in WAREHOUSE_PERMISSIONS:
			permission = Permission.objects.get(permission_code=code)
			RolePermission.objects.create(role=self.role, permission=permission)
		self.user = User.objects.create_user(email='warehouse@example.com', password='SecurePassword123!', first_name='Warehouse', last_name='Manager', role=self.role)
		department = Department.objects.create(department_name='Warehouse')
		designation = Designation.objects.create(designation_name='Warehouse Manager')
		self.employee = Employee.objects.create(
			user=self.user, employee_code='EMP-W-001', first_name='Warehouse', last_name='Manager',
			email='warehouse@example.com', phone='1234567890', department=department, designation=designation,
			joining_date=date(2026, 1, 1), employment_type=Employee.EmploymentType.FULL_TIME, base_salary=Decimal('50000'),
		)
		self.warehouse = Warehouse.objects.create(
			warehouse_code='WH-001', warehouse_name='Main Warehouse', location='Industrial Area',
			address='Warehouse Road', city='Pune', state='Maharashtra', pincode='411001',
			contact_number='1234567890', manager=self.employee,
		)
		self.category = ProductCategory.objects.create(category_code='CAT-001', category_name='Finished Product')
		self.product = Product.objects.create(
			sku='SKU-001', product_code='PROD-001', product_name='Bearing', category=self.category,
			unit=Product.Unit.PCS, unit_price=Decimal('100'), reorder_level=Decimal('20'), reorder_quantity=Decimal('50'),
		)
		self.supplier = Supplier.objects.create(
			supplier_code='SUP-001', supplier_name='Parts Supplier', contact_person='Supplier Contact',
			email='supplier@example.com', phone='1111111111', address='Supplier Road', city='Pune', state='Maharashtra', pincode='411002',
		)

	def create_order(self, status=Order.Status.CONFIRMED, quantity=Decimal('5')):
		customer_code = f'CUS-W-{Customer.objects.count() + 1:03d}'
		customer = Customer.objects.create(
			customer_code=customer_code, company_name='Customer', contact_person='Contact', email=f'{customer_code.lower()}@example.com',
			phone='2222222222', address='Customer Road', city='Pune', state='Maharashtra', pincode='411003', customer_type=Customer.CustomerType.BUSINESS,
		)
		order = Order.objects.create(
			order_number=f'SO-W-{Order.objects.count() + 1}', customer=customer, order_date=date(2026, 8, 20),
			priority=Order.Priority.NORMAL, delivery_address='Delivery Road', delivery_city='Pune', delivery_state='Maharashtra',
			delivery_pincode='411003', subtotal=Decimal('500'), tax_amount=Decimal('0'), discount_amount=Decimal('0'),
			total_amount=Decimal('500'), order_status=status, created_by=self.user,
		)
		OrderItem.objects.create(order=order, product=self.product, description='Bearing', quantity=quantity, unit_price=Decimal('100'), line_total=quantity * Decimal('100'))
		return order

	def test_warehouse_duplicate_code_and_product_duplicate_sku(self):
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Warehouse.objects.create(warehouse_code='WH-001', warehouse_name='Duplicate', location='x', address='x', city='x', state='x', pincode='x', contact_number='x', manager=self.employee)
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Product.objects.create(sku='SKU-001', product_code='PROD-002', product_name='Duplicate', category=self.category, unit_price=Decimal('1'))

	def test_category_supplier_and_inventory_creation(self):
		inventory = Inventory.objects.create(warehouse=self.warehouse, product=self.product, quantity_available=Decimal('10'), reorder_level=Decimal('20'))
		self.assertEqual(inventory.available_quantity, Decimal('10'))
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Inventory.objects.create(warehouse=self.warehouse, product=self.product)

	def test_purchase_order_receiving_updates_inventory_and_audit(self):
		purchase_order = PurchaseOrder.objects.create(
			purchase_order_number='PO-001', supplier=self.supplier, warehouse=self.warehouse, order_date=date(2026, 8, 20),
			subtotal=Decimal('1000'), total_amount=Decimal('1000'), created_by=self.user,
		)
		item = PurchaseOrderItem.objects.create(
			purchase_order=purchase_order, product=self.product, quantity_ordered=Decimal('10'), unit_price=Decimal('100'), line_total=Decimal('1000'),
		)
		receive_purchase_order(purchase_order, {item.pk: '10'}, self.user)
		self.assertEqual(Inventory.objects.get(warehouse=self.warehouse, product=self.product).quantity_available, Decimal('10.00'))
		self.assertEqual(StockTransaction.objects.filter(transaction_type=StockTransaction.TransactionType.PURCHASE).count(), 1)
		self.assertEqual(PurchaseOrder.objects.get(pk=purchase_order.pk).status, PurchaseOrder.Status.RECEIVED)

	def test_purchase_order_item_rejects_over_receiving(self):
		item = PurchaseOrderItem(purchase_order=PurchaseOrder(supplier=self.supplier, warehouse=self.warehouse), product=self.product, quantity_ordered=Decimal('1'), quantity_received=Decimal('2'), unit_price=Decimal('1'), line_total=Decimal('1'))
		with self.assertRaises(ValidationError):
			item.full_clean()

	def test_successful_and_insufficient_stock_reservation(self):
		Inventory.objects.create(warehouse=self.warehouse, product=self.product, quantity_available=Decimal('10'))
		order = self.create_order(quantity=Decimal('5'))
		reservation = reserve_stock_for_order(order, self.warehouse, self.user)
		self.assertEqual(reservation.status, 'RESERVED')
		self.assertEqual(Inventory.objects.get(pk=reservation.warehouse.inventory.first().pk).quantity_reserved, Decimal('5.00'))
		with self.assertRaises(ValueError):
			reserve_stock_for_order(self.create_order(quantity=Decimal('6')), self.warehouse, self.user)

	def test_release_and_allocate_stock(self):
		Inventory.objects.create(warehouse=self.warehouse, product=self.product, quantity_available=Decimal('10'))
		order = self.create_order(quantity=Decimal('5'))
		reserve_stock_for_order(order, self.warehouse, self.user)
		release_reserved_stock(order, self.user)
		self.assertEqual(Inventory.objects.get(warehouse=self.warehouse, product=self.product).quantity_reserved, Decimal('0.00'))
		order = self.create_order(quantity=Decimal('4'))
		reserve_stock_for_order(order, self.warehouse, self.user)
		allocate_stock_for_order(order, self.user)
		inventory = Inventory.objects.get(warehouse=self.warehouse, product=self.product)
		self.assertEqual(inventory.quantity_available, Decimal('6.00'))
		self.assertEqual(Order.objects.get(pk=order.pk).order_status, Order.Status.READY_FOR_DISPATCH)

	def test_low_stock_and_damage_adjustment(self):
		inventory = Inventory.objects.create(warehouse=self.warehouse, product=self.product, quantity_available=Decimal('5'), reorder_level=Decimal('20'))
		self.assertIn(inventory, low_stock_inventory())
		adjust_inventory(inventory, quantity_delta=Decimal('-2'), performed_by=self.user, reason='DAMAGE', remarks='Damaged goods')
		inventory.refresh_from_db()
		self.assertEqual(inventory.quantity_damaged, Decimal('2.00'))
		self.assertEqual(StockTransaction.objects.get(transaction_type=StockTransaction.TransactionType.DAMAGE).quantity, Decimal('2'))

	def test_stock_transfer_and_source_destination_validation(self):
		destination = Warehouse.objects.create(warehouse_code='WH-002', warehouse_name='Second Warehouse', location='Other Area', address='Road', city='Pune', state='Maharashtra', pincode='411004', contact_number='123', manager=self.employee)
		transfer = StockTransfer.objects.create(transfer_number='TR-001', source_warehouse=self.warehouse, destination_warehouse=destination, transfer_date=date(2026, 8, 20), initiated_by=self.user, status=StockTransfer.Status.APPROVED)
		StockTransferItem.objects.create(transfer=transfer, product=self.product, quantity=Decimal('3'))
		Inventory.objects.create(warehouse=self.warehouse, product=self.product, quantity_available=Decimal('5'))
		transfer_stock(transfer, self.user)
		receive_stock_transfer(transfer, self.user)
		self.assertEqual(Inventory.objects.get(warehouse=destination, product=self.product).quantity_available, Decimal('3.00'))
		invalid = StockTransfer(transfer_number='TR-002', source_warehouse=self.warehouse, destination_warehouse=self.warehouse, transfer_date=date(2026, 8, 20), initiated_by=self.user)
		with self.assertRaises(ValidationError):
			invalid.full_clean()

	def test_authentication_and_rbac(self):
		response = self.client.get(reverse('warehouse-product-list'))
		self.assertEqual(response.status_code, 401)
		self.client.force_authenticate(user=self.user)
		self.role.role_permissions.filter(permission__permission_code='MANAGE_PRODUCTS').delete()
		response = self.client.post(reverse('warehouse-product-list'), {'sku': 'SKU-002', 'product_code': 'PROD-002', 'product_name': 'Blocked', 'category': self.category.pk, 'unit_price': '1'}, format='json')
		self.assertEqual(response.status_code, 403)

# Create your tests here.
