from django.db import models


class Doctor(models.Model):
    """Doctor profile with specialization details."""

    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"
