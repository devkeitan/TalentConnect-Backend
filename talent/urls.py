from django.urls import path

from talent.views.dashboard import TalentDashboardView
from talent.views.portfolio import TalentPortfolioDetailView
from .views import TalentPortfolioView, TalentPortfolioListView, TalentMediaUploadView

urlpatterns = [
    path('dashboard/', TalentDashboardView.as_view(), name='talent-dashboard'),
]
