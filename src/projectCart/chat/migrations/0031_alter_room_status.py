# Generated by Django 4.2.4 on 2023-11-08 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0030_alter_room_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('closed', 'Closed'), ('waiting', 'Waiting')], default='waiting', max_length=20),
        ),
    ]
