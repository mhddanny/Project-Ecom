# Generated by Django 4.2.4 on 2023-12-29 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0035_remove_room_messages_alter_room_status_room_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('waiting', 'Waiting'), ('closed', 'Closed')], default='waiting', max_length=20),
        ),
    ]
