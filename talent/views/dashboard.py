from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from ..models import TalentPortfolio, TalentMedia
from organizer.models import BookingRequest, Review


class TalentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()

        try:
            portfolio = TalentPortfolio.objects.get(user=request.user)
        except TalentPortfolio.DoesNotExist:
            return Response({'error': 'Portfolio not found'}, status=404)

        bookings = BookingRequest.objects.filter(talent=portfolio)

        # Stats
        total_bookings    = bookings.count()
        pending_requests  = bookings.filter(status='pending').count()
        upcoming_events   = bookings.filter(
            status='accepted', event__date__gte=today
        ).count()
        reviews           = Review.objects.filter(talent=portfolio)
        avg_rating        = round(
            sum(r.rating for r in reviews) / len(reviews), 1
        ) if reviews else 0

        # Recent bookings — last 5
        recent = bookings.order_by('-created_at')[:5]
        recent_bookings = [{
            'id': b.id,
            'event': b.event.event_name,
            'organizer': b.organizer.organizer_profile.company_name
                         if hasattr(b.organizer, 'organizer_profile') else b.organizer.name,
            'date': b.event.date,
            'status': b.status,
        } for b in recent]

        # Upcoming events — accepted bookings with future dates
        upcoming = bookings.filter(
            status='accepted', event__date__gte=today
        ).order_by('event__date')[:5]
        upcoming_events_list = [{
            'id': b.id,
            'name': b.event.event_name,
            'date': b.event.date,
            'time': b.event.time,
            'location': b.event.location,
        } for b in upcoming]

        return Response({
            'stats': {
                'total_bookings':   total_bookings,
                'pending_requests': pending_requests,
                'upcoming_events':  upcoming_events,
                'avg_rating':       avg_rating,
            },
            'recent_bookings':  recent_bookings,
            'upcoming_events':  upcoming_events_list,
        })
