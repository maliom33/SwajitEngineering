from django.db import migrations


PERMISSIONS = [
    ('VIEW_FINANCE', 'View Finance'), ('MANAGE_INVOICES', 'Manage Invoices'), ('CREATE_INVOICE', 'Create Invoice'),
    ('MANAGE_PAYMENTS', 'Manage Payments'), ('RECORD_PAYMENT', 'Record Payment'), ('MANAGE_EXPENSES', 'Manage Expenses'),
    ('APPROVE_EXPENSES', 'Approve Expenses'), ('VIEW_FINANCIAL_TRANSACTIONS', 'View Financial Transactions'),
    ('MANAGE_FINANCIAL_ADJUSTMENTS', 'Manage Financial Adjustments'),
]


def seed_finance_permissions(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Role = apps.get_model('accounts', 'Role')
    RolePermission = apps.get_model('accounts', 'RolePermission')
    for code, name in PERMISSIONS:
        permission, _ = Permission.objects.get_or_create(permission_code=code, defaults={'permission_name': name, 'module': 'finance'})
        for role_code in ['SYSTEM_ADMIN', 'FINANCE_MANAGER']:
            role = Role.objects.filter(role_code=role_code).first()
            if role:
                RolePermission.objects.get_or_create(role=role, permission=permission)


def remove_finance_permissions(apps, schema_editor):
    apps.get_model('accounts', 'Permission').objects.filter(permission_code__in=[code for code, _ in PERMISSIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [('accounts', '0001_initial'), ('finance', '0001_initial')]
    operations = [migrations.RunPython(seed_finance_permissions, remove_finance_permissions)]