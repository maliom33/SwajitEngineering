from django.db import migrations


LEAVE_TYPES = [
    ('Casual Leave', 'Short personal or unplanned leave.', 12, True),
    ('Sick Leave', 'Leave for illness or medical recovery.', 12, True),
    ('Earned Leave', 'Planned annual leave entitlement.', 15, True),
]


def seed_hr_workforce_data(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Role = apps.get_model('accounts', 'Role')
    RolePermission = apps.get_model('accounts', 'RolePermission')
    LeaveType = apps.get_model('workforce', 'LeaveType')

    permission, _ = Permission.objects.get_or_create(
        permission_code='MANAGE_ATTENDANCE',
        defaults={
            'permission_name': 'Manage attendance and leave',
            'module': 'workforce',
            'description': 'Manage attendance and leave records.',
        },
    )
    for role_code in ('SYSTEM_ADMIN', 'HR_MANAGER'):
        role = Role.objects.filter(role_code=role_code).first()
        if role:
            RolePermission.objects.get_or_create(role=role, permission=permission)

    for leave_name, description, maximum_days, is_paid in LEAVE_TYPES:
        LeaveType.objects.get_or_create(
            leave_name=leave_name,
            defaults={
                'description': description,
                'maximum_days': maximum_days,
                'is_paid': is_paid,
                'is_active': True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('workforce', '0005_employee_management_permissions'),
    ]

    operations = [
        migrations.RunPython(seed_hr_workforce_data, migrations.RunPython.noop),
    ]
