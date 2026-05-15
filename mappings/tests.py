from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from doctors.models import Doctor
from patients.models import Patient

from .models import PatientDoctorMapping


class MappingAPITests(APITestCase):
    """Tests for Patient-Doctor Mapping endpoints."""

    list_url = "/api/mappings/"

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="securepass123")
        self.other_user = User.objects.create_user(username="otheruser", password="securepass123")
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

        self.patient = Patient.objects.create(name="John Doe", age=45, gender="M", created_by=self.user)
        self.other_patient = Patient.objects.create(
            name="Other Patient", age=30, gender="F", created_by=self.other_user
        )
        self.doctor = Doctor.objects.create(
            name="Dr. Sharma",
            specialization="Cardiology",
            experience_years=15,
            email="sharma@hospital.com",
        )

    def detail_url(self, pk):
        return f"/api/mappings/{pk}/"

    def patient_doctors_url(self, patient_id):
        return f"/api/mappings/{patient_id}/doctors/"

    # ── Create Mapping ────────────────────────────────────────

    def test_create_mapping(self):
        """POST assigns a doctor to the user's patient."""
        data = {"patient": self.patient.pk, "doctor": self.doctor.pk}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["patient_name"], "John Doe")
        self.assertEqual(response.data["doctor_name"], "Dr. Sharma")

    def test_create_mapping_other_users_patient(self):
        """Cannot assign a doctor to another user's patient."""
        data = {"patient": self.other_patient.pk, "doctor": self.doctor.pk}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_duplicate_mapping(self):
        """Duplicate patient-doctor mapping returns 400."""
        data = {"patient": self.patient.pk, "doctor": self.doctor.pk}
        self.client.post(self.list_url, data)
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ── List Mappings ─────────────────────────────────────────

    def test_list_mappings_only_own(self):
        """Users only see mappings for their own patients."""
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        PatientDoctorMapping.objects.create(patient=self.other_patient, doctor=self.doctor)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ── Patient-specific doctors ──────────────────────────────

    def test_get_doctors_for_patient(self):
        """GET /api/mappings/<patient_id>/doctors/ returns assigned doctors."""
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        response = self.client.get(self.patient_doctors_url(self.patient.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_doctors_for_other_users_patient(self):
        """Cannot view doctors for another user's patient."""
        response = self.client.get(self.patient_doctors_url(self.other_patient.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ── Delete Mapping ────────────────────────────────────────

    def test_delete_mapping(self):
        """DELETE removes a mapping and returns 204."""
        mapping = PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        response = self.client.delete(self.detail_url(mapping.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PatientDoctorMapping.objects.filter(pk=mapping.pk).exists())

    def test_delete_mapping_not_found(self):
        """DELETE a non-existent mapping returns 404."""
        response = self.client.delete(self.detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
