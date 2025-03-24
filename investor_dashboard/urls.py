from django.urls import path
from .views import ShortlistStartupView, PitchRequestView, InvestorShortlistedListView

urlpatterns = [
    path('shortlist/', ShortlistStartupView.as_view(), name='shortlist_startup'),
    path('request-pitch/', PitchRequestView.as_view(), name='request_pitch'),
    path('my-shortlist/', InvestorShortlistedListView.as_view(), name='my_shortlist'),
]
