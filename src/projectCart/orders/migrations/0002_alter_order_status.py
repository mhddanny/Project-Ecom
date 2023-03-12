# Generated by Django 4.1.5 on 2023-03-10 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('COMPLETED', 'COMPLETED'), ('NEW', 'NEW'), ('CANCELLED', 'CANCELLED')], default='NEW', max_length=10),
        ),
    ]