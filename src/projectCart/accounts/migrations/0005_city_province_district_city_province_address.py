# Generated by Django 4.2.4 on 2023-10-27 02:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_groups_account_is_superuser_and_more'),
    ]

    operations = [
        
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, verbose_name='Full Name')),
                ('phone', models.CharField(max_length=50, verbose_name='Phone')),
                ('address_line_1', models.CharField(max_length=150, verbose_name='Address Line 1')),
                ('address_line_2', models.CharField(max_length=150, verbose_name='Address Line 2')),
                ('delivery_intructions', models.CharField(blank=True, max_length=255, verbose_name='Delivery Intructions')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('default', models.BooleanField(default=False, verbose_name='Default')),
                ('district', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.district', verbose_name='District')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Address',
            },
        ),
    ]