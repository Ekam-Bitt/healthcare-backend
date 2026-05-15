from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Accepts ``name``, ``email``, and ``password``.  The *name* field is
    stored in Django's ``first_name`` column; ``username`` is derived
    from ``email`` when not supplied explicitly.
    """

    name = serializers.CharField(
        write_only=True,
        max_length=150,
        help_text="Full name of the user.",
    )
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("id", "name", "username", "email", "password")
        extra_kwargs = {
            "username": {"required": False},
        }

    def validate_email(self, value):
        """Ensure the email address is not already registered."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        name = validated_data.pop("name", "")
        username = validated_data.get("username") or validated_data["email"]
        user = User.objects.create_user(
            username=username,
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=name,
        )
        return user
