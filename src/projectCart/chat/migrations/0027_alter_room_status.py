# Generated by Django 4.2.4 on 2023-11-06 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0026_alter_room_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('closed', 'Closed'), ('waiting', 'Waiting'), ('active', 'Active')], default='waiting', max_length=20),
        ),
    ]
