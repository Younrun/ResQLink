from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

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

