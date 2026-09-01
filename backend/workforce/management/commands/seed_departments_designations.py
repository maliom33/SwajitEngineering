from django.core.management.base import BaseCommand

from workforce.models import Department, Designation


SEED_DATA = {
    'HR': ['HR Executive', 'HR Manager'],
    'Logistics': ['Logistics Executive', 'Logistics Manager', 'Driver', 'Delivery Executive'],
    'Warehouse': ['Warehouse Assistant', 'Warehouse Executive', 'Warehouse Manager', 'Store Keeper'],
    'Finance': ['Accountant', 'Finance Executive', 'Finance Manager'],
    'Sales': ['Sales Executive', 'Sales Manager'],
    'Production': ['Production Executive', 'Production Manager'],
    'Dispatch': ['Dispatch Executive', 'Dispatch Manager'],
}


class Command(BaseCommand):
    help = 'Create or update the standard workforce departments and designations.'

    def handle(self, *args, **options):
        for department_name, designation_names in SEED_DATA.items():
            department, _ = Department.objects.update_or_create(
                department_name=department_name,
                defaults={'is_active': True},
            )
            for designation_name in designation_names:
                Designation.objects.update_or_create(
                    designation_name=designation_name,
                    defaults={'department': department, 'is_active': True},
                )
        self.stdout.write(self.style.SUCCESS('Departments and designations seeded successfully.'))