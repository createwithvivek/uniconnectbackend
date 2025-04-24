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
        model = CustomUser,StudentProfile, MentorProfile, InvestorProfile
        fields = '__all__'

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            full_name=validated_data['full_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            role=validated_data['role'],
            
        )

        if validated_data['role'] == 'student':
            university = validated_data.get('university')
            city = validated_data.get('city')
            country = validated_data.get('country')
            StudentProfile.objects.create(user=user,city=city, country=country,university=university)

        elif validated_data['role'] == 'mentor':
            city = validated_data.get('city')   
            country = validated_data.get('country')
            MentorProfile.objects.create(user=user, city=city, country=country)
           
        elif validated_data['role'] == 'investor':
            investment_firm = validated_data.get('investment_firm')
            city = validated_data.get('city')
            country = validated_data.get('country')
            InvestorProfile.objects.create(user=user, city=city, country=country, investment_firm=investment_firm)
            
        return user


class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = UserSerializer()
