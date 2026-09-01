from django.db import migrations


PERMISSIONS = [
    ('MANAGE_RECRUITMENT', 'Manage Recruitment'),
    ('MANAGE_CANDIDATES', 'Manage Candidates'),
    ('MANAGE_JOB_POSITIONS', 'Manage Job Positions'),
    ('SCREEN_RESUMES', 'Screen Resumes'),
    ('MANAGE_INTERVIEWS', 'Manage Interviews'),
]


def seed_recruitment_permissions(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Role = apps.get_model('accounts', 'Role')
    RolePermission = apps.get_model('accounts', 'RolePermission')

    for code, name in PERMISSIONS:
        permission, _ = Permission.objects.get_or_create(
            permission_code=code,
            defaults={'permission_name': name, 'module': 'recruitment'},
        )
        for role_code in ['SYSTEM_ADMIN', 'HR_MANAGER']:
            role = Role.objects.filter(role_code=role_code).first()
            if role:
                RolePermission.objects.get_or_create(role=role, permission=permission)


def remove_recruitment_permissions(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Permission.objects.filter(permission_code__in=[code for code, _ in PERMISSIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('recruitment', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_recruitment_permissions, remove_recruitment_permissions),
    ]