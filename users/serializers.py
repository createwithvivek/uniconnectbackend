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
    university = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    investment_firm = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'username', 'email', 'phone', 'role', 'password',
                  'profile_picture', 'cover_photo', 'university', 'city', 'country', 'investment_firm')

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        university = validated_data.pop('university', None)
        city = validated_data.pop('city', None)
        country = validated_data.pop('country', None)
        investment_firm = validated_data.pop('investment_firm', None)

        user = CustomUser.objects.create_user(
            **validated_data,
            password=password,
            role=role
        )

        if role == 'student':
            StudentProfile.objects.create(user=user, university=university, city=city, country=country)
        elif role == 'mentor':
            MentorProfile.objects.create(user=user, city=city, country=country)
        elif role == 'investor':
            InvestorProfile.objects.create(user=user, city=city, country=country, investment_firm=investment_firm)

        return user



class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = UserSerializer()
