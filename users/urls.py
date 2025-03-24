from django.urls import path
from .views import (
    RegisterUserView, LoginView, 
    StudentDashboardView, MentorDashboardView, InvestorDashboardView
)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('mentor/dashboard/', MentorDashboardView.as_view(), name='mentor_dashboard'),
    path('investor/dashboard/', InvestorDashboardView.as_view(), name='investor_dashboard'),
]
