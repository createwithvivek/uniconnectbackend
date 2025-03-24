from rest_framework import serializers
from .models import Startup, Vote, WeeklyIdeaSubmission, InvestorShortlist

class StartupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startup
        fields = '__all__'
        read_only_fields = ('founder', 'created_at', 'updated_at', 'approved_by_mentor')

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class WeeklyIdeaSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyIdeaSubmission
        fields = '__all__'
        read_only_fields = ('user', 'submitted_at')

class InvestorShortlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorShortlist
        fields = '__all__'
