from rest_framework import serializers
from .models import InvestorShortlist, InvestorPitchRequest

class InvestorShortlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorShortlist
        fields = '__all__'

class InvestorPitchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorPitchRequest
        fields = '__all__'
