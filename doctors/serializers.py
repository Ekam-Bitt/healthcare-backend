from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor CRUD operations."""

    class Meta:
        model = Doctor
        fields = ("id", "name", "specialization", "experience_years", "email", "phone", "created_at")
        read_only_fields = ("id", "created_at")
