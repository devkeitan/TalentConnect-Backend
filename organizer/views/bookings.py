from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import BookingRequest
from ..serializers import BookingRequestSerializer


class BookingRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Organizer sees their sent requests
        bookings = BookingRequest.objects.filter(organizer=request.user)
        serializer = BookingRequestSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, booking_id):
        # Talent accepts or rejects
        try:
            booking = BookingRequest.objects.get(id=booking_id, talent__user=request.user)
        except BookingRequest.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status not in ['accepted', 'rejected']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = new_status
        booking.save()
        serializer = BookingRequestSerializer(booking)
        return Response(serializer.data)

class TalentBookingInboxView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Talent sees all incoming booking requests
        bookings = BookingRequest.objects.filter(
            talent__user=request.user
        ).order_by('-created_at')
        serializer = BookingRequestSerializer(bookings, many=True)
        return Response(serializer.data)

# Organizer cancels their own pending booking request
class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, booking_id):
        try:
            booking = BookingRequest.objects.get(id=booking_id, organizer=request.user)
        except BookingRequest.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        if booking.status != 'pending':
            return Response({'error': 'Only pending bookings can be cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        # Soft delete — keep the record, just mark as cancelled
        booking.status = 'cancelled'
        booking.save()
        return Response(status=status.HTTP_200_OK)
