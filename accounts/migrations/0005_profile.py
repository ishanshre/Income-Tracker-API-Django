# Generated by Django 4.1.3 on 2022-12-05 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='user/profile')),
                ('bio', models.TextField(max_length=1000)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('twitter', models.URLField(blank=True, max_length=255, null=True)),
                ('facebook', models.URLField(blank=True, max_length=255, null=True)),
                ('linkedIn', models.URLField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
