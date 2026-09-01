from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0004_otp_invalidated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpverification',
            name='target_hash',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]