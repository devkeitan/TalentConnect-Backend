from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'content', 'is_read', 'created_at']
        read_only_fields = ['sender', 'is_read', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    organizer_name = serializers.CharField(source='organizer.organizer_profile.company_name', read_only=True)
    talent_name = serializers.CharField(source='talent.portfolio.talent_name', read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    other_user_name = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'booking', 'organizer', 'talent',
            'other_user_name',
            'organizer_name', 'talent_name',
            'last_message', 'unread_count',
            'messages', 'created_at'
        ]

    def get_last_message(self, obj):
        last = obj.messages.last()
        return last.content if last else None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0
    

    def get_other_user_name(self, obj):
        request = self.context.get('request')
        if request and request.user == obj.organizer:
            return obj.talent.portfolio.talent_name
        return obj.organizer.organizer_profile.company_name

