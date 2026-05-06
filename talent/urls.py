from django.urls import path

from talent.views.dashboard import TalentDashboardView
from talent.views.portfolio import TalentPortfolioDetailView
from .views import TalentPortfolioView, TalentPortfolioListView, TalentMediaUploadView

urlpatterns = [
    path('portfolio/', TalentPortfolioView.as_view(), name='talent-portfolio'),
    path('portfolio/all/', TalentPortfolioListView.as_view(), name='talent-portfolio-list'),
    path('portfolio/media/', TalentMediaUploadView.as_view(), name='talent-media-upload'),
    path('portfolio/media/<int:media_id>/', TalentMediaUploadView.as_view()),
    path('portfolio/all/<int:portfolio_id>/', TalentPortfolioDetailView.as_view(), name='talent-portfolio-detail'),

]
