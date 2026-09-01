from django.core.management.base import BaseCommand

from accounts.models import Role


ROLES = [
    ('SYSTEM_ADMIN', 'System Administrator'),
    ('DIRECTOR', 'Director'),
    ('HR_MANAGER', 'HR Manager'),
    ('LOGISTICS_MANAGER', 'Logistics Manager'),
    ('WAREHOUSE_MANAGER', 'Warehouse Manager'),
    ('FINANCE_MANAGER', 'Finance Manager'),
    ('SALES_EXECUTIVE', 'Sales Executive'),
    ('DISPATCH_EXECUTIVE', 'Dispatch Executive'),
    ('DRIVER', 'Driver'),
    ('EMPLOYEE', 'Employee'),
]


class Command(BaseCommand):
    help = 'Create or update the initial system roles.'

    def handle(self, *args, **options):
        for role_code, role_name in ROLES:
            role, created = Role.objects.update_or_create(
                role_code=role_code,
                defaults={'role_name': role_name},
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{action} {role.role_name} ({role.role_code})')