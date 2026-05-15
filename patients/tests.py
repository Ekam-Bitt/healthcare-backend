from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Patient


class PatientAPITests(APITestCase):
    """Tests for Patient CRUD endpoints."""

    list_url = "/api/patients/"

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="securepass123")
        self.other_user = User.objects.create_user(username="otheruser", password="securepass123")
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        self.patient = Patient.objects.create(
            name="John Doe",
            age=45,
            gender="M",
            medical_history="Diabetes",
            created_by=self.user,
        )

    def detail_url(self, pk):
        return f"/api/patients/{pk}/"

    # ── Authentication ────────────────────────────────────────

    def test_unauthenticated_access_denied(self):
        """Unauthenticated requests get 401."""
        self.client.credentials()  # clear auth
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── List ──────────────────────────────────────────────────

    def test_list_patients_only_own(self):
        """Users only see patients they created."""
        Patient.objects.create(name="Other Patient", age=30, gender="F", created_by=self.other_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "John Doe")

    # ── Create ────────────────────────────────────────────────

    def test_create_patient(self):
        """Valid POST creates a patient and returns 201."""
        data = {"name": "Jane Smith", "age": 32, "gender": "F", "medical_history": "Asthma"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Jane Smith")
        self.assertEqual(response.data["created_by"], self.user.id)

    def test_create_patient_invalid(self):
        """POST with missing required fields returns 400."""
        response = self.client.post(self.list_url, {"name": "No Age"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ── Retrieve ──────────────────────────────────────────────

    def test_get_patient(self):
        """GET a specific patient by ID."""
        response = self.client.get(self.detail_url(self.patient.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "John Doe")

    def test_get_patient_not_found(self):
        """GET a non-existent patient returns 404."""
        response = self.client.get(self.detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_other_users_patient(self):
        """Cannot GET another user's patient."""
        other_patient = Patient.objects.create(name="Other", age=25, gender="M", created_by=self.other_user)
        response = self.client.get(self.detail_url(other_patient.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ── Update ────────────────────────────────────────────────

    def test_update_patient(self):
        """PUT updates patient fields (partial)."""
        response = self.client.put(self.detail_url(self.patient.pk), {"age": 46})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["age"], 46)

    # ── Delete ────────────────────────────────────────────────

    def test_delete_patient(self):
        """DELETE removes the patient and returns 204."""
        response = self.client.delete(self.detail_url(self.patient.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Patient.objects.filter(pk=self.patient.pk).exists())
