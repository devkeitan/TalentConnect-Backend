from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from ..models import Event, BookingRequest, Review
from talent.models import TalentPortfolio


class OrganizerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        # Stats
        all_events     = Event.objects.filter(organizer=user)
        all_bookings   = BookingRequest.objects.filter(organizer=user)

        active_events    = all_events.filter(date__gte=today).count()
        completed_events = all_events.filter(date__lt=today).count()
        pending_bookings = all_bookings.filter(status='pending').count()
        confirmed_talents = all_bookings.filter(status='accepted').count()

        # Recent activity — last 5 bookings
        recent_bookings = all_bookings.order_by('-created_at')[:5]
        recent_activity = []
        for b in recent_bookings:
            if b.status == 'pending':
                action = f"Booking request sent to {b.talent.talent_name}"
            elif b.status == 'accepted':
                action = f"{b.talent.talent_name} accepted your booking"
            elif b.status == 'rejected':
                action = f"{b.talent.talent_name} declined your booking"
            elif b.status == 'cancelled':
                action = f"Booking request to {b.talent.talent_name} cancelled"
            else:
                action = f"Booking updated for {b.talent.talent_name}"
            recent_activity.append({
                'id': b.id,
                'action': action,
                'status': b.status,
                'created_at': b.created_at,
            })

        # Recommended talents — top rated
        talents = TalentPortfolio.objects.all()[:5]
        recommended = []
        for t in talents:
            reviews = t.reviews.all()
            avg = round(sum(r.rating for r in reviews) / len(reviews), 1) if reviews else 0
            media = t.media.filter(media_type='photo').first()
            recommended.append({
                'id': t.id,
                'talent_name': t.talent_name,
                'service_type': t.service_type,
                'rating': avg,
                'avatar': media.file if media and media.file else '',
            })

        return Response({
            'stats': {
                'active_events':     active_events,
                'completed_events':  completed_events,
                'pending_bookings':  pending_bookings,
                'confirmed_talents': confirmed_talents,
            },
            'recent_activity': recent_activity,
            'recommended_talents': recommended,
        })
