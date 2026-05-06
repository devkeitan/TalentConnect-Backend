from django.db import models
from users.models import User


class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    event_name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name


BOOKING_STATUS = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
]

DURATION_CHOICES = [
    ('1', '1 hour'),
    ('2', '2 hours'),
    ('3', '3 hours'),
    ('4', '4 hours'),
    ('5', '5+ hours'),
]

class BookingRequest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='booking_requests')
    talent = models.ForeignKey('talent.TalentPortfolio', on_delete=models.CASCADE, related_name='booking_requests')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_requests')
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES, default='2')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organizer} → {self.talent} ({self.status})"
    