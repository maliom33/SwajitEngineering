from django.db import migrations


PERMISSIONS = [
    ('VIEW_ANALYTICS', 'View Analytics'), ('VIEW_EXECUTIVE_DASHBOARD', 'View Executive Dashboard'),
    ('VIEW_WORKFORCE_ANALYTICS', 'View Workforce Analytics'), ('VIEW_RECRUITMENT_ANALYTICS', 'View Recruitment Analytics'),
    ('VIEW_SALES_ANALYTICS', 'View Sales Analytics'), ('VIEW_WAREHOUSE_ANALYTICS', 'View Warehouse Analytics'),
    ('VIEW_LOGISTICS_ANALYTICS', 'View Logistics Analytics'), ('VIEW_DISPATCH_ANALYTICS', 'View Dispatch Analytics'),
    ('VIEW_FINANCE_ANALYTICS', 'View Finance Analytics'),
]


ROLE_PERMISSIONS = {
    'SYSTEM_ADMIN': [code for code, _ in PERMISSIONS],
    'DIRECTOR': ['VIEW_ANALYTICS', 'VIEW_EXECUTIVE_DASHBOARD', 'VIEW_WORKFORCE_ANALYTICS', 'VIEW_RECRUITMENT_ANALYTICS', 'VIEW_SALES_ANALYTICS', 'VIEW_WAREHOUSE_ANALYTICS', 'VIEW_LOGISTICS_ANALYTICS', 'VIEW_DISPATCH_ANALYTICS', 'VIEW_FINANCE_ANALYTICS'],
    'HR_MANAGER': ['VIEW_WORKFORCE_ANALYTICS', 'VIEW_RECRUITMENT_ANALYTICS'],
    'SALES_EXECUTIVE': ['VIEW_SALES_ANALYTICS'],
    'WAREHOUSE_MANAGER': ['VIEW_WAREHOUSE_ANALYTICS'],
    'LOGISTICS_MANAGER': ['VIEW_LOGISTICS_ANALYTICS'],
    'DISPATCH_EXECUTIVE': ['VIEW_DISPATCH_ANALYTICS'],
    'FINANCE_MANAGER': ['VIEW_FINANCE_ANALYTICS'],
}


def seed_analytics_permissions(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Role = apps.get_model('accounts', 'Role')
    RolePermission = apps.get_model('accounts', 'RolePermission')
    permissions = {}
    for code, name in PERMISSIONS:
        permissions[code], _ = Permission.objects.get_or_create(permission_code=code, defaults={'permission_name': name, 'module': 'analytics'})
    for role_code, codes in ROLE_PERMISSIONS.items():
        role = Role.objects.filter(role_code=role_code).first()
        if role:
            for code in codes:
                RolePermission.objects.get_or_create(role=role, permission=permissions[code])


def remove_analytics_permissions(apps, schema_editor):
    apps.get_model('accounts', 'Permission').objects.filter(permission_code__in=[code for code, _ in PERMISSIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [('accounts', '0001_initial')]
    operations = [migrations.RunPython(seed_analytics_permissions, remove_analytics_permissions)]