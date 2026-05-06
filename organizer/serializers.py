from rest_framework import serializers
from .models import OrganizerProfile, Event, BookingRequest, Review



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer', 'created_at']

