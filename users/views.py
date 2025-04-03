from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import CustomUser, StudentProfile, MentorProfile, InvestorProfile, Follow
from .serializers import (
    RegisterUserSerializer,
    UserSerializer,
    StudentProfileSerializer,
    MentorProfileSerializer,
    InvestorProfileSerializer,
    LoginResponseSerializer
)

class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
                'followers_count': user.follower_count(),
                'following_count': user.following_count(),
                'followers': [UserSerializer(follower).data for follower in user.get_followers()],
                'following': [UserSerializer(following).data for following in user.get_following()],
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class StudentDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'student':
            return Response({"error": "Access denied"}, status=403)
        profile = StudentProfile.objects.filter(user=user).first()
        data = {
            "user": UserSerializer(user).data,
            "profile": StudentProfileSerializer(profile).data if profile else {},
            "followers_count": user.follower_count(),
            "following_count": user.following_count(),
            "followers": [UserSerializer(follower).data for follower in user.get_followers()],
            "following": [UserSerializer(following).data for following in user.get_following()],
        }
        return Response(data)


class MentorDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'mentor':
            return Response({"error": "Access denied"}, status=403)
        profile = MentorProfile.objects.filter(user=user).first()
        data = {
            "user": UserSerializer(user).data,
            "profile": MentorProfileSerializer(profile).data if profile else {},
            "followers_count": user.follower_count(),
            "following_count": user.following_count(),
            "followers": [UserSerializer(follower).data for follower in user.get_followers()],
            "following": [UserSerializer(following).data for following in user.get_following()],
        }
        return Response(data)


class InvestorDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'investor':
            return Response({"error": "Access denied"}, status=403)
        profile = InvestorProfile.objects.filter(user=user).first()
        data = {
            "user": UserSerializer(user).data,
            "profile": InvestorProfileSerializer(profile).data if profile else {},
            "followers_count": user.follower_count(),
            "following_count": user.following_count(),
            "followers": [UserSerializer(follower).data for follower in user.get_followers()],
            "following": [UserSerializer(following).data for following in user.get_following()],
        }
        return Response(data)

class SearchUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('username', '')
        if not query:
            return Response({"error": "No search query provided"}, status=status.HTTP_400_BAD_REQUEST)

        users = CustomUser.objects.filter(username__icontains=query)
        data = UserSerializer(users, many=True).data
        return Response({"results": data}, status=status.HTTP_200_OK)
    
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user = request.user
        try:
            target_user = CustomUser.objects.get(id=user_id)
            if user != target_user:
                Follow.objects.get_or_create(follower=user, following=target_user)
                return Response({"message": "Followed successfully"}, status=status.HTTP_201_CREATED)
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        user = request.user
        try:
            target_user = CustomUser.objects.get(id=user_id)
            Follow.objects.filter(follower=user, following=target_user).delete()
            return Response({"message": "Unfollowed successfully"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class UpdateUserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    

    def put(self, request):
        user = request.user
        data = request.data

        

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        if 'cover_photo' in request.FILES:
            user.cover_photo = request.FILES['cover_photo']

        user.save()

        # Updating role-specific profiles
        if user.role == 'student':
            profile, created = StudentProfile.objects.get_or_create(user=user)
            serializer = StudentProfileSerializer(profile, data=data, partial=True)
        elif user.role == 'mentor':
            profile, created = MentorProfile.objects.get_or_create(user=user)
            serializer = MentorProfileSerializer(profile, data=data, partial=True)
        elif user.role == 'investor':
            profile, created = InvestorProfile.objects.get_or_create(user=user)
            serializer = InvestorProfileSerializer(profile, data=data, partial=True)
        else:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "user": UserSerializer(user).data, "profile": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)