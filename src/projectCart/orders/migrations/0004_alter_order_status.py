# Generated by Django 4.2.4 on 2023-10-27 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('COMPLETED', 'COMPLETED'), ('ACCEPTED', 'ACCEPTED'), ('CANCELLED', 'CANCELLED'), ('NEW', 'NEW')], default='NEW', max_length=10),
        ),
    ]
