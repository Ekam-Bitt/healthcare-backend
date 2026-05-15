from django.contrib import admin

from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "experience_years", "email", "created_at")
    list_filter = ("specialization",)
    search_fields = ("name", "email")
