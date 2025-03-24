from datetime import timezone
from urllib import response
from rest_framework import generics, permissions
from .models import Startup, Vote, WeeklyIdeaSubmission, InvestorShortlist
from .serializers import StartupSerializer, VoteSerializer, WeeklyIdeaSubmissionSerializer, InvestorShortlistSerializer
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

class StartupCreateView(generics.CreateAPIView):
    serializer_class = StartupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        last_submission = Startup.objects.filter(student=user).order_by('-created_at').first()
        if last_submission:
            days_since = (timezone.now() - last_submission.created_at).days
            if days_since < 7:
                return Response({"error": f"You can submit a new idea after {7 - days_since} more days."},
                                status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class StartupListView(generics.ListAPIView):
    queryset = Startup.objects.all().order_by('-created_at')
    serializer_class = StartupSerializer

class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WeeklyIdeaSubmissionCreateView(generics.CreateAPIView):
    serializer_class = WeeklyIdeaSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InvestorShortlistView(generics.CreateAPIView):
    serializer_class = InvestorShortlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(investor=self.request.user)
