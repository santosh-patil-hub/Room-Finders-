# models.py (in your accounts app)
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    TENANT = 'tenant'
    OWNER = 'owner'
    USER_TYPES = [
        (TENANT, 'Tenant'),
        (OWNER, 'Owner'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default=TENANT)

    def __str__(self):
        return self.username


# models.py (in your rooms app)
from django.conf import settings
from django.db import models

class Area(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

from django.db import models
from django.conf import settings

# Area model to represent different areas for rooms
class Area(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    room_type = models.CharField(choices=[
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('1rk', '1RK'),
        ('1bhk', '1BHK'),
        ('2bhk', '2BHK'),
        ('3bhk', '3BHK'),
    ], max_length=10)
    rent_per_month = models.DecimalField(decimal_places=2, max_digits=10)
    deposit = models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)
    light_bill_responsibility = models.CharField(choices=[
        ('owner', 'Room Owner'),
        ('tenant', 'Tenant')
    ], default='tenant', max_length=10)
    occupants_allowed = models.IntegerField(choices=[
        (1, '1 Person(s)'),
        (2, '2 Person(s)'),
        (3, '3 Person(s)'),
        (4, '4 Person(s)'),
        (5, '5 Person(s)'),
        (6, '6 Person(s)')
    ], default=1)
    address = models.CharField(max_length=255)
    landmark = models.CharField(blank=True, max_length=100)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)  
    house_number = models.CharField(max_length=10)
    floor_number = models.IntegerField(choices=[
        (0, '0 Floor'),
        (1, '1 Floor'),
        (2, '2 Floor'),
        (3, '3 Floor'),
        (4, '4 Floor'),
        (5, '5 Floor'),
        (6, '6 Floor')
    ])
    image1 = models.ImageField(upload_to='room_images/')
    image2 = models.ImageField(upload_to='room_images/')
    image3 = models.ImageField(upload_to='room_images/')
    image4 = models.ImageField(blank=True, null=True, upload_to='room_images/')
    image5 = models.ImageField(blank=True, null=True, upload_to='room_images/')
    owner_mobile_no = models.CharField(max_length=15)

    # New field for availability status
    availability_status = models.CharField(choices=[('available', 'Available'), ('booked', 'Booked')], 
                                           default='available', max_length=10)

    def __str__(self):
        return self.title
