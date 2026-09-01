from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('workforce', '0003_employee_activation'),
    ]

    operations = [
        migrations.AddField(
            model_name='designation',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='designations', to='workforce.department'),
        ),
    ]