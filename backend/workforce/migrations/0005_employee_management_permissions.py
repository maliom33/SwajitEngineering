from django.db import migrations


def seed_employee_management_permission(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Role = apps.get_model('accounts', 'Role')
    RolePermission = apps.get_model('accounts', 'RolePermission')

    permission, _ = Permission.objects.get_or_create(
        permission_code='MANAGE_EMPLOYEES',
        defaults={
            'permission_name': 'Manage employees',
            'module': 'workforce',
            'description': 'View and manage employee records.',
        },
    )
    for role_code in ('SYSTEM_ADMIN', 'HR_MANAGER'):
        role = Role.objects.filter(role_code=role_code).first()
        if role:
            RolePermission.objects.get_or_create(role=role, permission=permission)


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('workforce', '0004_designation_department'),
    ]

    operations = [
        migrations.RunPython(seed_employee_management_permission, migrations.RunPython.noop),
    ]