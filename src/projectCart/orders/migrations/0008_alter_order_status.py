# Generated by Django 4.2.4 on 2023-11-23 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CANCELLED', 'CANCELLED'), ('NEW', 'NEW'), ('ACCEPTED', 'ACCEPTED'), ('COMPLETED', 'COMPLETED')], default='NEW', max_length=10),
        ),
    ]
