from rest_framework import generics, permissions
from .models import Group, GroupMember, GroupPost
from .serializers import GroupSerializer, GroupMemberSerializer, GroupPostSerializer

class GroupCreateView(generics.CreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.save(creator=self.request.user)
        GroupMember.objects.create(group=group, user=self.request.user)

class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all().order_by('-created_at')
    serializer_class = GroupSerializer

class GroupJoinView(generics.CreateAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GroupPostCreateView(generics.CreateAPIView):
    serializer_class = GroupPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
