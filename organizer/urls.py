from django.urls import path

from organizer.views.dashboard import OrganizerDashboardView
from organizer.views.reviews import ReviewView, TalentReviewListView
from .views import OrganizerProfileView, OrganizerProfileListView, EventView, BookingRequestView, BookingStatusView, TalentBookingInboxView, CancelBookingView

urlpatterns = [
    
    path('profile/', OrganizerProfileView.as_view(), name='organizer-profile'),
    path('all/', OrganizerProfileListView.as_view(), name='organizer-list'),

    # New
    path('events/', EventView.as_view(), name='organizer-events'),
    path('events/<int:event_id>/', EventView.as_view(), name='organizer-event-delete'),
   
]
