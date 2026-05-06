from django.db import models
from users.models import User
from organizer.models import BookingRequest


class Conversation(models.Model):
    booking = models.OneToOneField(BookingRequest, on_delete=models.CASCADE, related_name='conversation')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizer_conversations')
    talent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='talent_conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation for Booking #{self.booking.id}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender} → Conversation #{self.conversation.id}"
