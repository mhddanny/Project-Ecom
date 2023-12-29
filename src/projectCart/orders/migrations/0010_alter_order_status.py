# Generated by Django 4.2.4 on 2023-12-29 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('COMPLETED', 'COMPLETED'), ('NEW', 'NEW'), ('CANCELLED', 'CANCELLED')], default='NEW', max_length=10),
        ),
    ]
