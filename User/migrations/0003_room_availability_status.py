# Generated by Django 4.2.10 on 2024-11-09 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_area_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='availability_status',
            field=models.CharField(choices=[('available', 'Available'), ('booked', 'Booked')], default='available', max_length=10),
        ),
    ]
