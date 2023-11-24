# Generated by Django 4.2.4 on 2023-11-23 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('COMPLETED', 'COMPLETED'), ('NEW', 'NEW'), ('CANCELLED', 'CANCELLED'), ('ACCEPTED', 'ACCEPTED')], default='NEW', max_length=10),
        ),
    ]
