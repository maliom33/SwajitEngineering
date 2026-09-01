from django.db import migrations, models


def create_employee_role(apps, schema_editor):
    Role = apps.get_model('accounts', 'Role')
    Role.objects.get_or_create(role_code='EMPLOYEE', defaults={'role_name': 'Employee'})


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('workforce', '0002_employee_code_sequence'),
    ]

    operations = [
        migrations.RunPython(create_employee_role, migrations.RunPython.noop),
        migrations.AddField(
            model_name='employee',
            name='activation_expires_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='activation_token_hash',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]