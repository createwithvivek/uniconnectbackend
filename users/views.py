from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import CustomUser, StudentProfile, MentorProfile, InvestorProfile
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
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
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
            "profile": StudentProfileSerializer(profile).data if profile else {}
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
            "profile": MentorProfileSerializer(profile).data if profile else {}
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
            "profile": InvestorProfileSerializer(profile).data if profile else {}
        }
        return Response(data)
