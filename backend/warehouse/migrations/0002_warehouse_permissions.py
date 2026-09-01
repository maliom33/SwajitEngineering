from django.db import migrations


PERMISSIONS = [
    ('MANAGE_WAREHOUSES', 'Manage Warehouses'),
    ('MANAGE_PRODUCTS', 'Manage Products'),
    ('MANAGE_SUPPLIERS', 'Manage Suppliers'),
    ('VIEW_INVENTORY', 'View Inventory'),
    ('MANAGE_INVENTORY', 'Manage Inventory'),
    ('MANAGE_PURCHASE_ORDERS', 'Manage Purchase Orders'),
    ('MANAGE_STOCK_TRANSFERS', 'Manage Stock Transfers'),
    ('ADJUST_INVENTORY', 'Adjust Inventory'),
    ('RECEIVE_STOCK', 'Receive Stock'),
    ('ALLOCATE_STOCK', 'Allocate Stock'),
]


def seed_warehouse_permissions(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Role = apps.get_model('accounts', 'Role')
    RolePermission = apps.get_model('accounts', 'RolePermission')

    for code, name in PERMISSIONS:
        permission, _ = Permission.objects.get_or_create(
            permission_code=code,
            defaults={'permission_name': name, 'module': 'warehouse'},
        )
        for role_code in ['SYSTEM_ADMIN', 'WAREHOUSE_MANAGER']:
            role = Role.objects.filter(role_code=role_code).first()
            if role:
                RolePermission.objects.get_or_create(role=role, permission=permission)


def remove_warehouse_permissions(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Permission.objects.filter(permission_code__in=[code for code, _ in PERMISSIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_warehouse_permissions, remove_warehouse_permissions),
    ]