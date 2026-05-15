from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Doctor


class DoctorAPITests(APITestCase):
    """Tests for Doctor CRUD endpoints."""

    list_url = "/api/doctors/"

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="securepass123")
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        self.doctor = Doctor.objects.create(
            name="Dr. Sharma",
            specialization="Cardiology",
            experience_years=15,
            email="sharma@hospital.com",
        )

    def detail_url(self, pk):
        return f"/api/doctors/{pk}/"

    # ── Authentication ────────────────────────────────────────

    def test_unauthenticated_access_denied(self):
        """Unauthenticated requests get 401."""
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── List ──────────────────────────────────────────────────

    def test_list_doctors(self):
        """GET returns all doctors."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ── Create ────────────────────────────────────────────────

    def test_create_doctor(self):
        """POST creates a doctor and returns 201."""
        data = {
            "name": "Dr. Patel",
            "specialization": "Pulmonology",
            "experience_years": 10,
            "email": "patel@hospital.com",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Doctor.objects.count(), 2)

    def test_create_doctor_duplicate_email(self):
        """POST with duplicate email returns 400."""
        data = {
            "name": "Dr. Duplicate",
            "specialization": "General",
            "experience_years": 5,
            "email": "sharma@hospital.com",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ── Retrieve ──────────────────────────────────────────────

    def test_get_doctor(self):
        """GET a specific doctor by ID."""
        response = self.client.get(self.detail_url(self.doctor.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Dr. Sharma")

    def test_get_doctor_not_found(self):
        """GET a non-existent doctor returns 404."""
        response = self.client.get(self.detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ── Update ────────────────────────────────────────────────

    def test_update_doctor(self):
        """PUT updates doctor fields."""
        response = self.client.put(self.detail_url(self.doctor.pk), {"experience_years": 16})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["experience_years"], 16)

    # ── Delete ────────────────────────────────────────────────

    def test_delete_doctor(self):
        """DELETE removes the doctor and returns 204."""
        response = self.client.delete(self.detail_url(self.doctor.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Doctor.objects.filter(pk=self.doctor.pk).exists())
