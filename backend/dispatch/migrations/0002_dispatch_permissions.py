from django.db import migrations


PERMISSIONS = [
    ('MANAGE_DISPATCH', 'Manage Dispatch'), ('VIEW_DISPATCH', 'View Dispatch'),
    ('CREATE_DISPATCH', 'Create Dispatch'), ('PREPARE_DISPATCH', 'Prepare Dispatch'),
    ('GENERATE_DELIVERY_CHALLAN', 'Generate Delivery Challan'), ('HANDOVER_DISPATCH', 'Handover Dispatch'),
    ('UPDATE_DISPATCH_STATUS', 'Update Dispatch Status'), ('VIEW_DISPATCH_HISTORY', 'View Dispatch History'),
]


def seed_dispatch_permissions(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Role = apps.get_model('accounts', 'Role')
    RolePermission = apps.get_model('accounts', 'RolePermission')
    for code, name in PERMISSIONS:
        permission, _ = Permission.objects.get_or_create(permission_code=code, defaults={'permission_name': name, 'module': 'dispatch'})
        for role_code in ['SYSTEM_ADMIN', 'DISPATCH_EXECUTIVE']:
            role = Role.objects.filter(role_code=role_code).first()
            if role:
                RolePermission.objects.get_or_create(role=role, permission=permission)


def remove_dispatch_permissions(apps, schema_editor):
    apps.get_model('accounts', 'Permission').objects.filter(permission_code__in=[code for code, _ in PERMISSIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [('accounts', '0001_initial'), ('dispatch', '0001_initial')]
    operations = [migrations.RunPython(seed_dispatch_permissions, remove_dispatch_permissions)]