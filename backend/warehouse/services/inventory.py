from decimal import Decimal

from django.db import transaction
from django.db.models import F
from django.utils import timezone

from sales.models import Order

from ..models import (
    Inventory,
    PurchaseOrder,
    StockReservation,
    StockReservationItem,
    StockTransaction,
    StockTransfer,
)


def _inventory_for_update(warehouse, product):
    inventory, _ = Inventory.objects.select_for_update().get_or_create(
        warehouse=warehouse,
        product=product,
        defaults={'reorder_level': product.reorder_level},
    )
    return Inventory.objects.select_for_update().get(pk=inventory.pk)


def record_stock_transaction(*, inventory, transaction_type, quantity, performed_by, reference_type='', reference_id='', remarks=''):
    return StockTransaction.objects.create(
        warehouse=inventory.warehouse,
        product=inventory.product,
        transaction_type=transaction_type,
        quantity=quantity,
        balance_after=inventory.quantity_available,
        performed_by=performed_by,
        reference_type=reference_type,
        reference_id=str(reference_id),
        remarks=remarks,
    )


@transaction.atomic
def receive_purchase_order(purchase_order, received_quantities, performed_by):
    purchase_order = PurchaseOrder.objects.select_for_update().get(pk=purchase_order.pk)
    if purchase_order.status in [PurchaseOrder.Status.CANCELLED, PurchaseOrder.Status.CLOSED, PurchaseOrder.Status.RECEIVED]:
        raise ValueError('This purchase order cannot receive more stock.')

    items = {item.pk: item for item in purchase_order.items.select_for_update()}
    for item_id, quantity in received_quantities.items():
        item = items.get(int(item_id))
        quantity = Decimal(str(quantity))
        if not item or quantity <= 0 or item.quantity_received + quantity > item.quantity_ordered:
            raise ValueError('Received quantity is invalid for the purchase order item.')

    for item_id, raw_quantity in received_quantities.items():
        item = items[int(item_id)]
        quantity = Decimal(str(raw_quantity))
        inventory = _inventory_for_update(purchase_order.warehouse, item.product)
        inventory.quantity_available += quantity
        inventory.last_stock_update = timezone.now()
        inventory.save(update_fields=['quantity_available', 'last_stock_update', 'updated_at'])
        item.quantity_received += quantity
        item.save(update_fields=['quantity_received', 'updated_at'])
        record_stock_transaction(
            inventory=inventory,
            transaction_type=StockTransaction.TransactionType.PURCHASE,
            quantity=quantity,
            performed_by=performed_by,
            reference_type='PurchaseOrder',
            reference_id=purchase_order.pk,
        )

    all_received = all(item.quantity_received == item.quantity_ordered for item in items.values())
    purchase_order.status = PurchaseOrder.Status.RECEIVED if all_received else PurchaseOrder.Status.PARTIALLY_RECEIVED
    purchase_order.save(update_fields=['status', 'updated_at'])
    return purchase_order


@transaction.atomic
def reserve_stock_for_order(order, warehouse, reserved_by):
    order = Order.objects.select_for_update().prefetch_related('items').get(pk=order.pk)
    if order.order_status not in [Order.Status.CONFIRMED, Order.Status.PROCESSING]:
        raise ValueError('Only confirmed or processing orders can reserve stock.')
    if hasattr(order, 'stock_reservation') and order.stock_reservation.status != StockReservation.Status.RELEASED:
        return order.stock_reservation

    reservation = StockReservation.objects.create(order=order, warehouse=warehouse, reserved_by=reserved_by)
    for item in order.items.all():
        if not item.product_id:
            raise ValueError('Every order item must reference a Warehouse product.')
        inventory = _inventory_for_update(warehouse, item.product)
        if inventory.available_quantity < item.quantity:
            raise ValueError(f'Insufficient stock for product {item.product.sku}.')
        inventory.quantity_reserved += item.quantity
        inventory.save(update_fields=['quantity_reserved', 'updated_at'])
        StockReservationItem.objects.create(reservation=reservation, product=item.product, quantity=item.quantity)
    return reservation


@transaction.atomic
def release_reserved_stock(order, released_by):
    order = Order.objects.select_for_update().get(pk=order.pk)
    reservation = getattr(order, 'stock_reservation', None)
    if not reservation or reservation.status != StockReservation.Status.RESERVED:
        return reservation
    for item in reservation.items.select_related('product').select_for_update():
        inventory = _inventory_for_update(reservation.warehouse, item.product)
        if inventory.quantity_reserved < item.quantity:
            raise ValueError('Reserved stock cannot become negative.')
        inventory.quantity_reserved -= item.quantity
        inventory.save(update_fields=['quantity_reserved', 'updated_at'])
        record_stock_transaction(
            inventory=inventory,
            transaction_type=StockTransaction.TransactionType.ORDER_RELEASE,
            quantity=item.quantity,
            performed_by=released_by,
            reference_type='SalesOrder',
            reference_id=order.pk,
        )
    reservation.status = StockReservation.Status.RELEASED
    reservation.save(update_fields=['status', 'updated_at'])
    return reservation


@transaction.atomic
def allocate_stock_for_order(order, allocated_by):
    order = Order.objects.select_for_update().get(pk=order.pk)
    reservation = getattr(order, 'stock_reservation', None)
    if not reservation or reservation.status != StockReservation.Status.RESERVED:
        raise ValueError('A reserved order is required before allocation.')
    for item in reservation.items.select_related('product').select_for_update():
        inventory = _inventory_for_update(reservation.warehouse, item.product)
        inventory.quantity_reserved -= item.quantity
        inventory.quantity_available -= item.quantity
        inventory.save(update_fields=['quantity_reserved', 'quantity_available', 'updated_at'])
        record_stock_transaction(
            inventory=inventory,
            transaction_type=StockTransaction.TransactionType.ORDER_ALLOCATION,
            quantity=item.quantity,
            performed_by=allocated_by,
            reference_type='SalesOrder',
            reference_id=order.pk,
        )
    reservation.status = StockReservation.Status.ALLOCATED
    reservation.save(update_fields=['status', 'updated_at'])
    order.order_status = Order.Status.READY_FOR_DISPATCH
    order.save(update_fields=['order_status', 'updated_at'])
    return reservation


def low_stock_inventory():
    return Inventory.objects.select_related('warehouse', 'product').filter(
        quantity_available__lte=F('reorder_level') + F('quantity_reserved'),
    )


@transaction.atomic
def adjust_inventory(inventory, *, quantity_delta, performed_by, reason, remarks=''):
    inventory = Inventory.objects.select_for_update().get(pk=inventory.pk)
    quantity_delta = Decimal(str(quantity_delta))
    next_quantity = inventory.quantity_available + quantity_delta
    if next_quantity < inventory.quantity_reserved:
        raise ValueError('Adjustment cannot reduce available stock below reserved stock.')
    inventory.quantity_available = next_quantity
    if reason == StockTransaction.TransactionType.DAMAGE and quantity_delta < 0:
        inventory.quantity_damaged += abs(quantity_delta)
    inventory.save(update_fields=['quantity_available', 'quantity_damaged', 'updated_at'])
    return record_stock_transaction(
        inventory=inventory,
        transaction_type=StockTransaction.TransactionType.ADJUSTMENT if reason != 'DAMAGE' else StockTransaction.TransactionType.DAMAGE,
        quantity=abs(quantity_delta), performed_by=performed_by, reference_type='Adjustment', remarks=remarks,
    )


@transaction.atomic
def transfer_stock(transfer, transferred_by):
    transfer = StockTransfer.objects.select_for_update().get(pk=transfer.pk)
    if transfer.status not in [StockTransfer.Status.APPROVED, StockTransfer.Status.REQUESTED]:
        raise ValueError('Only approved or requested transfers can begin.')
    for item in transfer.items.select_related('product').select_for_update():
        inventory = _inventory_for_update(transfer.source_warehouse, item.product)
        if inventory.available_quantity < item.quantity:
            raise ValueError(f'Insufficient stock for product {item.product.sku}.')
        inventory.quantity_available -= item.quantity
        inventory.save(update_fields=['quantity_available', 'updated_at'])
        record_stock_transaction(
            inventory=inventory, transaction_type=StockTransaction.TransactionType.TRANSFER_OUT,
            quantity=item.quantity, performed_by=transferred_by, reference_type='StockTransfer', reference_id=transfer.pk,
        )
    transfer.status = StockTransfer.Status.IN_TRANSIT
    transfer.save(update_fields=['status', 'updated_at'])
    return transfer


@transaction.atomic
def receive_stock_transfer(transfer, received_by):
    transfer = StockTransfer.objects.select_for_update().get(pk=transfer.pk)
    if transfer.status != StockTransfer.Status.IN_TRANSIT:
        raise ValueError('Only in-transit transfers can be received.')
    for item in transfer.items.select_related('product').select_for_update():
        inventory = _inventory_for_update(transfer.destination_warehouse, item.product)
        inventory.quantity_available += item.quantity
        inventory.save(update_fields=['quantity_available', 'updated_at'])
        item.received_quantity = item.quantity
        item.save(update_fields=['received_quantity'])
        record_stock_transaction(
            inventory=inventory, transaction_type=StockTransaction.TransactionType.TRANSFER_IN,
            quantity=item.quantity, performed_by=received_by, reference_type='StockTransfer', reference_id=transfer.pk,
        )
    transfer.status = StockTransfer.Status.RECEIVED
    transfer.received_at = timezone.now()
    transfer.save(update_fields=['status', 'received_at', 'updated_at'])
    return transfer