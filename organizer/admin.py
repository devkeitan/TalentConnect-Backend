from django.contrib import admin

from organizer.models import BookingRequest, Event, OrganizerProfile, Review

# Register your models here.
admin.site.register(OrganizerProfile)
admin.site.register(Event)
admin.site.register(BookingRequest)
admin.site.register(Review)