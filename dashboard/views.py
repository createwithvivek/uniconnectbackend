from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from startups.models import Startup
from investor_dashboard.models import InvestorShortlist
from groups.models import Group
from tweets.models import Post
from users.models import CustomUser
from .serializers import StartupSerializer, PostSerializer, GroupSerializer, InvestorShortlistSerializer, UserBasicSerializer

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = user.role

        if role == 'student':
            # Student Dashboard Data
            startups = Startup.objects.filter(owner=user)
            startups_data = StartupSerializer(startups, many=True).data
            posts = Post.objects.filter(author=user)
            posts_data = PostSerializer(posts, many=True).data
            groups = Group.objects.filter(members=user)
            groups_data = GroupSerializer(groups, many=True).data

            return Response({
                'role': role,
                'my_startups': startups_data,
                'my_posts': posts_data,
                'groups_joined': groups_data
            })

        elif role == 'mentor':
            # Mentor Dashboard Data
            groups_created = Group.objects.filter(created_by=user)
            groups_data = GroupSerializer(groups_created, many=True).data
            all_startups = Startup.objects.all()
            startups_data = StartupSerializer(all_startups, many=True).data

            return Response({
                'role': role,
                'groups_created': groups_data,
                'all_startups_to_review': startups_data
            })

        elif role == 'investor':
            # Investor Dashboard Data
            shortlisted = InvestorShortlist.objects.filter(investor=user)
            shortlisted_data = InvestorShortlistSerializer(shortlisted, many=True).data
            trending_startups = Startup.objects.order_by('-votes')[:5]
            trending_data = StartupSerializer(trending_startups, many=True).data

            return Response({
                'role': role,
                'shortlisted_startups': shortlisted_data,
                'trending_startups': trending_data
            })

        else:
            return Response({'message': 'Invalid user role'}, status=400)
