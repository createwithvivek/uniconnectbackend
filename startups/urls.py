from django.urls import path
from .views import (
    StartupCreateView, StartupListView, VoteCreateView,
    WeeklyIdeaSubmissionCreateView, InvestorShortlistView
)

urlpatterns = [
    path('create/', StartupCreateView.as_view(), name='create_startup'),
    path('list/', StartupListView.as_view(), name='list_startups'),
    path('vote/', VoteCreateView.as_view(), name='vote_startup'),
    path('weekly-idea/', WeeklyIdeaSubmissionCreateView.as_view(), name='weekly_idea'),
    path('shortlist/', InvestorShortlistView.as_view(), name='investor_shortlist'),
]
