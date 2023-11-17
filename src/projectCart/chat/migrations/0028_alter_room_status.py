# Generated by Django 4.2.4 on 2023-11-06 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0027_alter_room_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('closed', 'Closed'), ('waiting', 'Waiting')], default='waiting', max_length=20),
        ),
    ]
