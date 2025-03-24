from rest_framework import generics, permissions
from .models import InvestorShortlist, InvestorPitchRequest
from .serializers import InvestorShortlistSerializer, InvestorPitchRequestSerializer

class ShortlistStartupView(generics.CreateAPIView):
    serializer_class = InvestorShortlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(investor=self.request.user)

class PitchRequestView(generics.CreateAPIView):
    serializer_class = InvestorPitchRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(investor=self.request.user)

class InvestorShortlistedListView(generics.ListAPIView):
    serializer_class = InvestorShortlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InvestorShortlist.objects.filter(investor=self.request.user)
