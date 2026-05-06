from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from organizer.models import BookingRequest


class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conversations = Conversation.objects.filter(
            organizer=request.user
        ) | Conversation.objects.filter(
            talent=request.user
        )
        conversations = conversations.order_by('-created_at')
        serializer = ConversationSerializer(conversations, many=True, context={'request': request})
        return Response(serializer.data)


class ConversationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)

        # Mark messages as read
        conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data)


class GetOrCreateConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = BookingRequest.objects.get(id=booking_id)
        except BookingRequest.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        conversation, created = Conversation.objects.get_or_create(
            booking=booking,
            defaults={
                'organizer': booking.organizer,
                'talent': booking.talent.user
            }
        )
        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
