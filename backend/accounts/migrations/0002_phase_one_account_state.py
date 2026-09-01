from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('accounts', '0001_initial')]
    operations = [
        migrations.AddField('user', 'is_first_login', models.BooleanField(default=False)),
        migrations.AddField('user', 'email_verified', models.BooleanField(default=False)),
        migrations.AddField('user', 'phone_verified', models.BooleanField(default=False)),
    ]