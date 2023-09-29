# Generated by Django 4.2.4 on 2023-08-22 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'NEW'), ('COMPLETED', 'COMPLETED'), ('ACCEPTED', 'ACCEPTED'), ('CANCELLED', 'CANCELLED')], default='NEW', max_length=10),
        ),
    ]