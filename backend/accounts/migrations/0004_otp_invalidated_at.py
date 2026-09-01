from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0003_otp_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpverification',
            name='invalidated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]