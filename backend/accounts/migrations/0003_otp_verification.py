from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_phase_one_account_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(choices=[('EMAIL_VERIFICATION', 'Email verification'), ('MOBILE_VERIFICATION', 'Mobile verification')], max_length=30)),
                ('channel', models.CharField(choices=[('EMAIL', 'Email'), ('SMS', 'SMS')], max_length=10)),
                ('code_hash', models.CharField(max_length=64)),
                ('expires_at', models.DateTimeField()),
                ('attempt_count', models.PositiveSmallIntegerField(default=0)),
                ('max_attempts', models.PositiveSmallIntegerField(default=5)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('verified_at', models.DateTimeField(blank=True, null=True)),
                ('last_sent_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otp_verifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['user', 'purpose', 'is_verified'], name='accounts_ot_user_id_45e62c_idx'),
                    models.Index(fields=['expires_at'], name='accounts_ot_expires_b7415d_idx'),
                ],
            },
        ),
    ]