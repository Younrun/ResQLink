from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('normal', 'Normal User'),
        ('paid', 'Paid User'),
        ('hospital', 'Hospital'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='normal')

    # track subscription expiry or location details here
    subscription_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

class HospitalProfile(models.Model):
    """
    Extra data for hospital accounts:
      - bed capacity / current availability
      - medication stock
      - location, etc.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Example resource fields:
    available_beds = models.PositiveIntegerField(default=0)
    medication_stock = models.PositiveIntegerField(default=0)
    
    # Example location data: either a text address or lat/long fields
    location = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Hospital Profile of {self.user.username}"