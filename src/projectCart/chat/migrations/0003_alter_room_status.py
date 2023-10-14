# Generated by Django 4.2.4 on 2023-10-13 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_room_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('active', 'Active'), ('close', 'Close')], default='waiting', max_length=20),
        ),
    ]
