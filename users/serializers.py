from rest_framework import serializers
from .models import CustomUser, StudentProfile, MentorProfile, InvestorProfile
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone', 'role', 'profile_picture', 'cover_photo')


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'


class MentorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorProfile
        fields = '__all__'


class InvestorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorProfile
        fields = '__all__'


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('student', 'Student'), ('mentor', 'Mentor'), ('investor', 'Investor')])

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password', 'role', 'profile_picture', 'cover_photo')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            role=validated_data['role'],
            profile_picture=validated_data.get('profile_picture'),
            cover_photo=validated_data.get('cover_photo')
        )
        return user


class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = UserSerializer()
