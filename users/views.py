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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction, IntegrityError
from django.contrib.auth.hashers import make_password

from .models import CustomUser, StudentProfile, MentorProfile, InvestorProfile

class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        try:
            with transaction.atomic():
                role = data.get('role')
                if role not in ['student', 'mentor', 'investor']:
                    return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

                username = data.get('username')
                email = data.get('email')
                phone = data.get('phone')
                password = data.get('password')
                full_name = data.get('full_name')

                # Basic validation
                if not all([username, email, phone, password, role]):
                    return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

                # Create user
                user = CustomUser.objects.create(
                    username=username,
                    email=email,
                    phone=phone,
                    full_name=full_name,
                    role=role,
                    password=make_password(password)
                )

                # Handle profile based on role
                if role == 'student':
                    StudentProfile.objects.create(
                        user=user,
                        university=data.get('university'),
                        degree=data.get('degree'),
                        graduation_year=data.get('graduation_year'),
                        skills=data.get('skills'),
                        city=data.get('city', 'N/A'),
                        country=data.get('country', 'N/A'),
                    )

                elif role == 'mentor':
                    MentorProfile.objects.create(
                        user=user,
                        work_experience=data.get('work_experience'),
                        company=data.get('company'),
                        industry=data.get('industry'),
                        linkedin=data.get('linkedin'),
                        portfolio=data.get('portfolio'),
                        expertise_areas=data.get('expertise_areas'),
                        open_for_mentorship=data.get('open_for_mentorship', True),
                        availability=data.get('availability'),
                        city=data.get('city', 'N/A'),
                        country=data.get('country', 'N/A'),
                    )

                elif role == 'investor':
                    InvestorProfile.objects.create(
                        user=user,
                        investment_firm=data.get('investment_firm'),
                        investment_categories=data.get('investment_categories'),
                        min_investment=data.get('min_investment'),
                        max_investment=data.get('max_investment'),
                        stage_of_interest=data.get('stage_of_interest'),
                        city=data.get('city', 'N/A'),
                        country=data.get('country', 'N/A'),
                    )

                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            return Response({'error': 'User with that email or phone already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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