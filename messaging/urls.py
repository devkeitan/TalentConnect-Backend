from django.urls import path
from .views import ConversationListView, ConversationDetailView, GetOrCreateConversationView

urlpatterns = [
    path('conversations/', ConversationListView.as_view(), name='conversations'),
    path('conversations/<int:conversation_id>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/booking/<int:booking_id>/', GetOrCreateConversationView.as_view(), name='get-or-create-conversation'),
]
