from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient CRUD operations."""

    class Meta:
        model = Patient
        fields = ("id", "name", "age", "gender", "medical_history", "created_by", "created_at")
        read_only_fields = ("id", "created_by", "created_at")
