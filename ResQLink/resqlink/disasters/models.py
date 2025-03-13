from django.db import models
from accounts.models import CustomUser

class DisasterReport(models.Model):
    DISASTER_TYPES = [
        ('Flood', 'Flood'),
        ('Earthquake', 'Earthquake'),
        ('Fire', 'Fire'),
        ('Tornado', 'Tornado'),
        ('Hurricane', 'Hurricane'),
        ('Landslide', 'Landslide'),
        ('Tsunami', 'Tsunami'),
        ('Drought', 'Drought'),
        ('Volcanic Eruption', 'Volcanic Eruption'),
        ('Extreme Heat', 'Extreme Heat'),
        ('Snowstorm', 'Snowstorm'),
        ('Thunderstorm', 'Thunderstorm'),
    ]

    SEVERITY_LEVELS = [
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    disaster_type = models.CharField(max_length=30, choices=DISASTER_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS, default='Moderate')
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    image = models.ImageField(upload_to='disaster_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disaster_type} ({self.severity}) reported by {self.user.username}"
