from django.urls import path

from organizer.views.dashboard import OrganizerDashboardView
from organizer.views.reviews import ReviewView, TalentReviewListView
from .views import OrganizerProfileView, OrganizerProfileListView, EventView, BookingRequestView, BookingStatusView, TalentBookingInboxView, CancelBookingView

urlpatterns = [
    
    path('profile/', OrganizerProfileView.as_view(), name='organizer-profile'),
    path('all/', OrganizerProfileListView.as_view(), name='organizer-list'),

    # New
    path('bookings/', BookingRequestView.as_view(), name='booking-request'),
    path('bookings/<int:booking_id>/status/', BookingStatusView.as_view(), name='booking-status'),
    path('bookings/inbox/', TalentBookingInboxView.as_view(), name='talent-booking-inbox'),
     path('bookings/<int:booking_id>/cancel/', CancelBookingView.as_view(), name='booking-cancel'),
]
