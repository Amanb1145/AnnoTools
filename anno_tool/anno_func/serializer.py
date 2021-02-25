from rest_framework import serializers
from .models import AnnoTool


class AnnoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnoTool
        fields = '__all__'