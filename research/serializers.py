from rest_framework import serializers

from .models import ResearchInformation


class ResearchInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchInformation
        fields = "__all__"
        lookup = 'number'

class DataResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchInformation
        exclude = ['id', 'created_at', 'updated_at']