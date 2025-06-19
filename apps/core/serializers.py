# apps/core/serializers.py

from rest_framework import serializers
from apps.core.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'access_key','encryption_key', 'created_at']
        read_only_fields = ['id', 'created_at']
