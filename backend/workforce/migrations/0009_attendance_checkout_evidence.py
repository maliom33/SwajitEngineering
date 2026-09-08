from django.db import migrations, models
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):
    dependencies = [('workforce', '0008_attendance_photo_location')]

    operations = [
        migrations.AddField(
            model_name='attendance', name='check_out_photo',
            field=models.ImageField(blank=True, null=True, upload_to='attendance/check-out/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='attendance', name='check_out_latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('-90')), django.core.validators.MaxValueValidator(Decimal('90'))]),
        ),
        migrations.AddField(
            model_name='attendance', name='check_out_longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('-180')), django.core.validators.MaxValueValidator(Decimal('180'))]),
        ),
        migrations.AddField(
            model_name='attendance', name='total_work_minutes',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]