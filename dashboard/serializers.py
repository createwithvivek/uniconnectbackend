from rest_framework import serializers
from startups.models import Startup
from tweets.models import Post
from groups.models import Group
from investor_dashboard.models import InvestorShortlist
from users.models import CustomUser

class StartupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startup
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class InvestorShortlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorShortlist
        fields = '__all__'

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']
