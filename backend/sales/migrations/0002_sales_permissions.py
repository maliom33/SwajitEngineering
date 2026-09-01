from django.db import migrations


PERMISSIONS = [
    ('MANAGE_CUSTOMERS', 'Manage Customers'),
    ('VIEW_CUSTOMERS', 'View Customers'),
    ('MANAGE_CUSTOMER_COMMUNICATION', 'Manage Customer Communication'),
    ('MANAGE_QUOTATIONS', 'Manage Quotations'),
    ('CREATE_SALES_ORDER', 'Create Sales Order'),
    ('VIEW_SALES_ORDERS', 'View Sales Orders'),
    ('UPDATE_SALES_ORDER', 'Update Sales Order'),
    ('MANAGE_ORDER_STATUS', 'Manage Order Status'),
]


def seed_sales_permissions(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Role = apps.get_model('accounts', 'Role')
    RolePermission = apps.get_model('accounts', 'RolePermission')

    for code, name in PERMISSIONS:
        permission, _ = Permission.objects.get_or_create(
            permission_code=code,
            defaults={'permission_name': name, 'module': 'sales'},
        )
        for role_code in ['SYSTEM_ADMIN', 'SALES_EXECUTIVE']:
            role = Role.objects.filter(role_code=role_code).first()
            if role:
                RolePermission.objects.get_or_create(role=role, permission=permission)


def remove_sales_permissions(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Permission.objects.filter(permission_code__in=[code for code, _ in PERMISSIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_sales_permissions, remove_sales_permissions),
    ]