from django.db import migrations


PERMISSIONS = [
    ('MANAGE_VEHICLES', 'Manage Vehicles'), ('MANAGE_DRIVERS', 'Manage Drivers'),
    ('VIEW_FLEET', 'View Fleet'), ('MANAGE_VEHICLE_MAINTENANCE', 'Manage Vehicle Maintenance'),
    ('MANAGE_ROUTES', 'Manage Routes'), ('MANAGE_DELIVERIES', 'Manage Deliveries'),
    ('ASSIGN_DELIVERIES', 'Assign Deliveries'), ('UPDATE_DELIVERY_STATUS', 'Update Delivery Status'),
    ('VIEW_DELIVERY_TRACKING', 'View Delivery Tracking'),
]


def seed_logistics_permissions(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Role = apps.get_model('accounts', 'Role')
    RolePermission = apps.get_model('accounts', 'RolePermission')
    for code, name in PERMISSIONS:
        permission, _ = Permission.objects.get_or_create(permission_code=code, defaults={'permission_name': name, 'module': 'logistics'})
        for role_code in ['SYSTEM_ADMIN', 'LOGISTICS_MANAGER']:
            role = Role.objects.filter(role_code=role_code).first()
            if role:
                RolePermission.objects.get_or_create(role=role, permission=permission)


def remove_logistics_permissions(apps, schema_editor):
    apps.get_model('accounts', 'Permission').objects.filter(permission_code__in=[code for code, _ in PERMISSIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [('accounts', '0001_initial'), ('logistics', '0001_initial')]
    operations = [migrations.RunPython(seed_logistics_permissions, remove_logistics_permissions)]