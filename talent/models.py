from django.db import models
from users.models import User


class TalentPortfolio(models.Model):
    SERVICE_CHOICES = [
        ('singer', 'Singer'),
        ('dancer', 'Dancer'),
        ('band', 'Band'),
        ('dj', 'DJ'),
        ('emcee', 'Emcee'),
        ('comedian', 'Comedian'),
        ('musician', 'Musician'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    talent_name = models.CharField(max_length=200)        # can be individual or group name
    location = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.talent_name}"


class TalentMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]

    portfolio = models.ForeignKey(TalentPortfolio, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=50)
    file = models.URLField(max_length=500)  # ← changed from FileField
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.portfolio.talent_name} - {self.media_type}"
