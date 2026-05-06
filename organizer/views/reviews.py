from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Review, BookingRequest
from ..serializers import ReviewSerializer


class ReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Organizer sees all reviews they've submitted
        reviews = Review.objects.filter(organizer=request.user)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Prevent duplicate reviews on same booking
        booking_id = request.data.get('booking')
        if Review.objects.filter(booking_id=booking_id, organizer=request.user).exists():
            return Response({'error': 'You already reviewed this booking'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TalentReviewListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, talent_id):
        # Anyone can see a talent's reviews
        reviews = Review.objects.filter(talent_id=talent_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
