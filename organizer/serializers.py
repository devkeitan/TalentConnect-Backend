from rest_framework import serializers
from .models import OrganizerProfile, Event, BookingRequest, Review


class OrganizerProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = OrganizerProfile
        fields = [
            'id', 'name', 'email',
            'company_name', 'description',
            'website', 'location',
            'profile_picture',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer', 'created_at']


class BookingRequestSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.event_name', read_only=True)
    event_type = serializers.CharField(source='event.event_type', read_only=True)
    event_date = serializers.DateField(source='event.date', read_only=True)
    event_time = serializers.TimeField(source='event.time', read_only=True)
    event_location = serializers.CharField(source='event.location', read_only=True)
    talent_name = serializers.CharField(source='talent.talent_name', read_only=True)
    organizer_company = serializers.CharField(source='organizer.organizer_profile.company_name', read_only=True)

    class Meta:
        model = BookingRequest
        fields = [
            'id', 'event', 'talent', 'organizer',
            'event_name', 'event_type', 'event_date', 'event_time', 'event_location',
            'talent_name', 'organizer_company',
            'duration', 'message', 'status', 'created_at'
        ]
        read_only_fields = ['organizer', 'status', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    talent_name = serializers.CharField(source='talent.talent_name', read_only=True)
    organizer_company = serializers.CharField(source='organizer.organizer_profile.company_name', read_only=True)
    event_name = serializers.CharField(source='booking.event.event_name', read_only=True)
    event_type = serializers.CharField(source='booking.event.event_type', read_only=True)
    event_date = serializers.DateField(source='booking.event.date', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'booking', 'talent', 'organizer',
            'talent_name', 'organizer_company', 'event_name', 'event_type', 
            'event_date', 'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['organizer', 'created_at']
