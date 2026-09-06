from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from logistics.services.delivery_service import update_delivery_status
from warehouse.models import StockReservation

from sales.models import Order, OrderStatusHistory

from ..models import DeliveryChallan, Dispatch, DispatchItem, DispatchStatusHistory


ACTIVE_STATUSES = [Dispatch.Status.SCHEDULED, Dispatch.Status.PREPARING, Dispatch.Status.READY, Dispatch.Status.HANDED_OVER, Dispatch.Status.DISPATCHED]


def _allocation_for(dispatch):
    reservation = getattr(dispatch.order, 'stock_reservation', None)
    if not reservation or reservation.status != StockReservation.Status.ALLOCATED or reservation.warehouse_id != dispatch.warehouse_id:
        raise ValueError('Warehouse stock must be allocated for this order and warehouse.')
    return {item.product_id: item.quantity for item in reservation.items.all()}


@transaction.atomic
def create_dispatch(*, order, delivery, warehouse, dispatch_number, prepared_by, scheduled_dispatch_date, remarks=''):
    if order.order_status != 'READY_FOR_DISPATCH':
        raise ValueError('Only orders ready for dispatch can create a dispatch.')
    if delivery.order_id != order.pk:
        raise ValueError('Delivery must belong to the selected order.')
    if delivery.delivery_status in ['DELIVERED', 'CANCELLED', 'FAILED']:
        raise ValueError('Delivery is not active.')
    _allocation_for(type('DispatchReference', (), {'order': order, 'warehouse_id': warehouse.pk})())
    if Dispatch.objects.filter(order=order, dispatch_status__in=ACTIVE_STATUSES).exists():
        raise ValueError('An active dispatch already exists for this order.')
    dispatch = Dispatch.objects.create(dispatch_number=dispatch_number, order=order, delivery=delivery, warehouse=warehouse, scheduled_dispatch_date=scheduled_dispatch_date, prepared_by=prepared_by, remarks=remarks)
    DispatchStatusHistory.objects.create(dispatch=dispatch, new_status=Dispatch.Status.SCHEDULED, changed_by=prepared_by)
    return dispatch


@transaction.atomic
def prepare_dispatch(dispatch, *, items, changed_by):
    dispatch = Dispatch.objects.select_for_update().get(pk=dispatch.pk)
    if dispatch.dispatch_status == Dispatch.Status.CANCELLED:
        raise ValueError('Cancelled dispatches cannot be prepared.')
    allocation = _allocation_for(dispatch)
    if not items:
        raise ValueError('At least one dispatch item is required.')
    DispatchItem.objects.filter(dispatch=dispatch).delete()
    for entry in items:
        product_id = int(entry['product'])
        quantity = Decimal(str(entry['quantity']))
        if product_id not in allocation or quantity <= 0 or quantity > allocation[product_id]:
            raise ValueError('Dispatch quantity exceeds allocated quantity.')
        DispatchItem.objects.create(dispatch=dispatch, product_id=product_id, quantity=quantity, package_count=int(entry.get('package_count', 1)), remarks=entry.get('remarks', ''))
    previous = dispatch.dispatch_status
    dispatch.dispatch_status = Dispatch.Status.READY
    dispatch.save(update_fields=['dispatch_status', 'updated_at'])
    DispatchStatusHistory.objects.create(dispatch=dispatch, previous_status=previous, new_status=Dispatch.Status.READY, changed_by=changed_by)
    return dispatch


@transaction.atomic
def generate_delivery_challan(dispatch, *, issued_by, challan_number=None):
    dispatch = Dispatch.objects.select_for_update().get(pk=dispatch.pk)
    dispatch = Dispatch.objects.select_related('order', 'delivery__driver__employee', 'delivery__vehicle').get(pk=dispatch.pk)
    if dispatch.dispatch_status != Dispatch.Status.READY or not dispatch.items.exists():
        raise ValueError('Dispatch must be ready and contain items.')
    if hasattr(dispatch, 'challan'):
        return dispatch.challan
    driver = dispatch.delivery.driver
    vehicle = dispatch.delivery.vehicle
    if not driver or not vehicle:
        raise ValueError('A driver and vehicle are required to generate the challan.')
    if not challan_number:
        challan_number = f'DC-{timezone.now():%Y%m%d%H%M%S}-{dispatch.pk}'
    total_quantity = sum((item.quantity for item in dispatch.items.all()), Decimal('0'))
    return DeliveryChallan.objects.create(challan_number=challan_number, dispatch=dispatch, challan_date=timezone.localdate(), issued_by=issued_by, vehicle_number_snapshot=vehicle.vehicle_number, driver_name_snapshot=f'{driver.employee.first_name} {driver.employee.last_name}', delivery_address=dispatch.order.delivery_address, total_items=dispatch.items.count(), total_quantity=total_quantity)


@transaction.atomic
def handover_dispatch(dispatch, *, handed_over_by):
    dispatch = Dispatch.objects.select_for_update().get(pk=dispatch.pk)
    if dispatch.dispatch_status != Dispatch.Status.READY or not dispatch.delivery.driver_id or not dispatch.delivery.vehicle_id:
        raise ValueError('Dispatch must be ready with an assigned driver and vehicle.')
    if not hasattr(dispatch, 'challan') or dispatch.challan.status == DeliveryChallan.Status.CANCELLED:
        raise ValueError('A valid delivery challan is required.')
    previous = dispatch.dispatch_status
    dispatch.handed_over_by = handed_over_by
    dispatch.dispatch_status = Dispatch.Status.HANDED_OVER
    dispatch.save(update_fields=['handed_over_by', 'dispatch_status', 'updated_at'])
    DispatchStatusHistory.objects.create(dispatch=dispatch, previous_status=previous, new_status=Dispatch.Status.HANDED_OVER, changed_by=handed_over_by)
    return dispatch


@transaction.atomic
def confirm_dispatch(dispatch, *, confirmed_by):
    dispatch = Dispatch.objects.select_for_update().get(pk=dispatch.pk)
    if dispatch.dispatch_status != Dispatch.Status.HANDED_OVER:
        raise ValueError('Only handed-over dispatches can be confirmed.')
    previous = dispatch.dispatch_status
    dispatch.dispatch_status = Dispatch.Status.DISPATCHED
    dispatch.actual_dispatch_date = timezone.now()
    dispatch.save(update_fields=['dispatch_status', 'actual_dispatch_date', 'updated_at'])
    DispatchStatusHistory.objects.create(dispatch=dispatch, previous_status=previous, new_status=Dispatch.Status.DISPATCHED, changed_by=confirmed_by)
    order = Order.objects.select_for_update().get(pk=dispatch.order_id)
    if order.order_status == Order.Status.READY_FOR_DISPATCH:
        order.order_status = Order.Status.DISPATCHED
        order.save(update_fields=['order_status', 'updated_at'])
        OrderStatusHistory.objects.create(order=order, previous_status=Order.Status.READY_FOR_DISPATCH, new_status=Order.Status.DISPATCHED, changed_by=confirmed_by, remarks='Dispatch confirmed.')
    delivery = dispatch.delivery
    if delivery.delivery_status == 'CREATED':
        update_delivery_status(delivery, new_status='ASSIGNED', changed_by=confirmed_by, remarks='Dispatch confirmed with assigned driver and vehicle.')
        update_delivery_status(delivery, new_status='PICKED_UP', changed_by=confirmed_by, remarks='Shipment handed over by Dispatch.')
        update_delivery_status(delivery, new_status='IN_TRANSIT', changed_by=confirmed_by, remarks='Dispatch confirmed.')
    elif delivery.delivery_status == 'ASSIGNED':
        update_delivery_status(delivery, new_status='PICKED_UP', changed_by=confirmed_by, remarks='Shipment handed over by Dispatch.')
        update_delivery_status(delivery, new_status='IN_TRANSIT', changed_by=confirmed_by, remarks='Dispatch confirmed.')
    return dispatch


@transaction.atomic
def cancel_dispatch(dispatch, *, cancelled_by, remarks=''):
    dispatch = Dispatch.objects.select_for_update().get(pk=dispatch.pk)
    if dispatch.dispatch_status in [Dispatch.Status.DISPATCHED, Dispatch.Status.CANCELLED]:
        raise ValueError('This dispatch cannot be cancelled.')
    previous = dispatch.dispatch_status
    dispatch.dispatch_status = Dispatch.Status.CANCELLED
    dispatch.remarks = remarks or dispatch.remarks
    dispatch.save(update_fields=['dispatch_status', 'remarks', 'updated_at'])
    DispatchStatusHistory.objects.create(dispatch=dispatch, previous_status=previous, new_status=Dispatch.Status.CANCELLED, changed_by=cancelled_by, remarks=remarks)
    return dispatch