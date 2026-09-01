from django.db import migrations, models


def initialize_employee_code_sequence(apps, schema_editor):
    Employee = apps.get_model('workforce', 'Employee')
    EmployeeCodeSequence = apps.get_model('workforce', 'EmployeeCodeSequence')

    highest_number = 0
    for employee_code in Employee.objects.values_list('employee_code', flat=True):
        if employee_code.startswith('EMP') and employee_code[3:].isdigit():
            highest_number = max(highest_number, int(employee_code[3:]))

    EmployeeCodeSequence.objects.create(pk=1, next_number=highest_number + 1)


class Migration(migrations.Migration):
    dependencies = [
        ('workforce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeCodeSequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('next_number', models.PositiveIntegerField(default=1)),
            ],
            options={
                'verbose_name': 'employee code sequence',
                'verbose_name_plural': 'employee code sequence',
            },
        ),
        migrations.RunPython(initialize_employee_code_sequence, migrations.RunPython.noop),
    ]
