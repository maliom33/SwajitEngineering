from django.db import migrations


ROLE_ACCESS = {
    'SALES_EXECUTIVE': ['VIEW_INVENTORY', 'ALLOCATE_STOCK'],
    'LOGISTICS_MANAGER': ['VIEW_INVENTORY'],
    'DIRECTOR': ['VIEW_INVENTORY'],
}


def grant_warehouse_role_access(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Role = apps.get_model('accounts', 'Role')
    RolePermission = apps.get_model('accounts', 'RolePermission')

    for role_code, permission_codes in ROLE_ACCESS.items():
        role = Role.objects.filter(role_code=role_code).first()
        if not role:
            continue
        for permission_code in permission_codes:
            permission = Permission.objects.filter(permission_code=permission_code).first()
            if permission:
                RolePermission.objects.get_or_create(role=role, permission=permission)


class Migration(migrations.Migration):
    dependencies = [
        ('warehouse', '0002_warehouse_permissions'),
    ]

    operations = [
        migrations.RunPython(grant_warehouse_role_access, migrations.RunPython.noop),
    ]