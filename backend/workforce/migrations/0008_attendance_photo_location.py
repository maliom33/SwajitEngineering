from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):
	dependencies = [
		('workforce', '0007_workflow_permissions'),
	]

	operations = [
		migrations.AddField(
			model_name='attendance',
			name='photo',
			field=models.ImageField(blank=True, null=True, upload_to='attendance/%Y/%m/%d/'),
		),
		migrations.AddField(
			model_name='attendance',
			name='latitude',
			field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)]),
		),
		migrations.AddField(
			model_name='attendance',
			name='longitude',
			field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)]),
		),
	]