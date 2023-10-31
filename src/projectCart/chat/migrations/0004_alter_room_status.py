# Generated by Django 4.2.4 on 2023-10-23 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_room_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('active', 'Active'), ('closed', 'Closed')], default='waiting', max_length=20),
        ),
    ]