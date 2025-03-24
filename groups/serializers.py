from rest_framework import serializers
from .models import Group, GroupMember, GroupPost

class GroupPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GroupPost
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()
    posts = GroupPostSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'

    def get_members_count(self, obj):
        return obj.members.count()

class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = '__all__'
