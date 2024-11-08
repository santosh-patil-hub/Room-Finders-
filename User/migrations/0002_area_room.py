# Generated by Django 4.2.10 on 2024-11-06 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('room_type', models.CharField(choices=[('single', 'Single Room'), ('double', 'Double Room'), ('1rk', '1RK'), ('1bhk', '1BHK'), ('2bhk', '2BHK'), ('3bhk', '3BHK')], max_length=10)),
                ('rent_per_month', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deposit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('light_bill_responsibility', models.CharField(choices=[('owner', 'Room Owner'), ('tenant', 'Tenant')], default='tenant', max_length=10)),
                ('occupants_allowed', models.IntegerField(choices=[(1, '1 Person(s)'), (2, '2 Person(s)'), (3, '3 Person(s)'), (4, '4 Person(s)'), (5, '5 Person(s)'), (6, '6 Person(s)')], default=1)),
                ('address', models.CharField(max_length=255)),
                ('landmark', models.CharField(blank=True, max_length=100)),
                ('house_number', models.CharField(max_length=10)),
                ('floor_number', models.IntegerField(choices=[(0, '0 Floor'), (1, '1 Floor'), (2, '2 Floor'), (3, '3 Floor'), (4, '4 Floor'), (5, '5 Floor'), (6, '6 Floor')])),
                ('image1', models.ImageField(upload_to='room_images/')),
                ('image2', models.ImageField(upload_to='room_images/')),
                ('image3', models.ImageField(upload_to='room_images/')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='room_images/')),
                ('image5', models.ImageField(blank=True, null=True, upload_to='room_images/')),
                ('owner_mobile_no', models.CharField(max_length=15)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.area')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]