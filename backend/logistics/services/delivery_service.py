from django.db import transaction
from django.utils import timezone

from ..models import Delivery, DeliveryStatusHistory, Driver, Vehicle


ASSIGNABLE_DRIVER_STATES = {Driver.AvailabilityStatus.AVAILABLE}
ASSIGNABLE_VEHICLE_STATES = {Vehicle.Status.AVAILABLE}


@transaction.atomic
def create_delivery(*, order, delivery_number, created_by, route=None, expected_delivery_time=None, delivery_notes=''):
    if order.order_status != 'READY_FOR_DISPATCH':
        raise ValueError('A delivery can only be created for an order ready for dispatch.')
    if Delivery.objects.filter(order=order, delivery_status__in=[Delivery.Status.CREATED, Delivery.Status.ASSIGNED, Delivery.Status.PICKED_UP, Delivery.Status.IN_TRANSIT, Delivery.Status.OUT_FOR_DELIVERY]).exists():
        raise ValueError('This order already has an active delivery.')
    delivery = Delivery.objects.create(
        delivery_number=delivery_number, order=order, route=route,
        expected_delivery_time=expected_delivery_time, delivery_notes=delivery_notes,
        created_by=created_by,
    )
    DeliveryStatusHistory.objects.create(delivery=delivery, new_status=Delivery.Status.CREATED, changed_by=created_by)
    return delivery


@transaction.atomic
def assign_delivery(delivery, *, driver, vehicle, changed_by):
    delivery = Delivery.objects.select_for_update().get(pk=delivery.pk)
    driver = Driver.objects.select_for_update().get(pk=driver.pk)
    vehicle = Vehicle.objects.select_for_update().get(pk=vehicle.pk)
    if delivery.delivery_status != Delivery.Status.CREATED:
        raise ValueError('Only created deliveries can be assigned.')
    if driver.availability_status not in ASSIGNABLE_DRIVER_STATES:
        raise ValueError('Driver is not available for assignment.')
    if vehicle.status not in ASSIGNABLE_VEHICLE_STATES:
        raise ValueError('Vehicle is not available for assignment.')
    delivery.driver = driver
    delivery.vehicle = vehicle
    delivery.assigned_at = timezone.now()
    delivery.delivery_status = Delivery.Status.ASSIGNED
    delivery.save(update_fields=['driver', 'vehicle', 'assigned_at', 'delivery_status', 'updated_at'])
    driver.availability_status = Driver.AvailabilityStatus.ASSIGNED
    driver.save(update_fields=['availability_status', 'updated_at'])
    vehicle.status = Vehicle.Status.ASSIGNED
    vehicle.save(update_fields=['status', 'updated_at'])
    DeliveryStatusHistory.objects.create(delivery=delivery, previous_status=Delivery.Status.CREATED, new_status=Delivery.Status.ASSIGNED, changed_by=changed_by)
    return delivery


TRANSITIONS = {
    Delivery.Status.CREATED: {Delivery.Status.ASSIGNED, Delivery.Status.CANCELLED},
    Delivery.Status.ASSIGNED: {Delivery.Status.PICKED_UP, Delivery.Status.CANCELLED, Delivery.Status.ON_HOLD},
    Delivery.Status.PICKED_UP: {Delivery.Status.IN_TRANSIT, Delivery.Status.CANCELLED},
    Delivery.Status.IN_TRANSIT: {Delivery.Status.OUT_FOR_DELIVERY, Delivery.Status.ON_HOLD},
    Delivery.Status.OUT_FOR_DELIVERY: {Delivery.Status.DELIVERED, Delivery.Status.FAILED, Delivery.Status.ON_HOLD},
    Delivery.Status.ON_HOLD: {Delivery.Status.ASSIGNED, Delivery.Status.CANCELLED},
    Delivery.Status.DELIVERED: set(),
    Delivery.Status.FAILED: set(),
    Delivery.Status.CANCELLED: set(),
}


@transaction.atomic
def update_delivery_status(delivery, *, new_status, changed_by, location_description='', remarks=''):
    delivery = Delivery.objects.select_for_update().get(pk=delivery.pk)
    if new_status not in Delivery.Status.values:
        raise ValueError('Invalid delivery status.')
    if new_status not in TRANSITIONS.get(delivery.delivery_status, set()):
        raise ValueError(f'Cannot transition from {delivery.delivery_status} to {new_status}.')
    previous_status = delivery.delivery_status
    delivery.delivery_status = new_status
    if new_status == Delivery.Status.PICKED_UP:
        delivery.pickup_time = timezone.now()
    if new_status == Delivery.Status.DELIVERED:
        delivery.actual_delivery_time = timezone.now()
    delivery.save(update_fields=['delivery_status', 'pickup_time', 'actual_delivery_time', 'updated_at'])
    if delivery.driver_id:
        driver = Driver.objects.select_for_update().get(pk=delivery.driver_id)
        driver.availability_status = Driver.AvailabilityStatus.ON_DELIVERY if new_status in [Delivery.Status.PICKED_UP, Delivery.Status.IN_TRANSIT, Delivery.Status.OUT_FOR_DELIVERY] else Driver.AvailabilityStatus.AVAILABLE if new_status in [Delivery.Status.DELIVERED, Delivery.Status.FAILED, Delivery.Status.CANCELLED] else driver.availability_status
        driver.save(update_fields=['availability_status', 'updated_at'])
    if delivery.vehicle_id:
        vehicle = Vehicle.objects.select_for_update().get(pk=delivery.vehicle_id)
        vehicle.status = Vehicle.Status.IN_TRANSIT if new_status in [Delivery.Status.PICKED_UP, Delivery.Status.IN_TRANSIT, Delivery.Status.OUT_FOR_DELIVERY] else Vehicle.Status.AVAILABLE if new_status in [Delivery.Status.DELIVERED, Delivery.Status.FAILED, Delivery.Status.CANCELLED] else vehicle.status
        vehicle.save(update_fields=['status', 'updated_at'])
    DeliveryStatusHistory.objects.create(delivery=delivery, previous_status=previous_status, new_status=new_status, changed_by=changed_by, location_description=location_description, remarks=remarks)
    return delivery