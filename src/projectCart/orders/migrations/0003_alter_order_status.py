# Generated by Django 4.1.5 on 2023-03-12 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('NEW', 'NEW'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED')], default='NEW', max_length=10),
        ),
    ]
