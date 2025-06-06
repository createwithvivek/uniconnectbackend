from django.urls import path
from .views import (
    RegisterUserView, LoginView, 
    StudentDashboardView, MentorDashboardView, InvestorDashboardView,
    SearchUserView, FollowUserView, UpdateUserProfileView
)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('mentor/dashboard/', MentorDashboardView.as_view(), name='mentor_dashboard'),
    path('investor/dashboard/', InvestorDashboardView.as_view(), name='investor_dashboard'),
    path('search/', SearchUserView.as_view(), name='search_user'),
    path('follow/', FollowUserView.as_view(), name='follow_user'),
    path('update-profile/', UpdateUserProfileView.as_view(), name='update_profile'),
]
