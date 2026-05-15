from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from patients.models import Patient

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer


class MappingListCreateView(APIView):
    """
    GET  → List all mappings for patients owned by the authenticated user.
    POST → Assign a doctor to one of the authenticated user's patients.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        mappings = PatientDoctorMapping.objects.filter(patient__created_by=request.user)
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Ensure the patient belongs to the authenticated user
        patient_id = request.data.get("patient")
        if patient_id:
            if not Patient.objects.filter(pk=patient_id, created_by=request.user).exists():
                return Response(
                    {"error": "Patient not found or does not belong to you"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        serializer = PatientDoctorMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MappingDetailView(APIView):
    """
    GET    → Retrieve a specific mapping.
    DELETE → Remove a patient-doctor assignment.
    """

    permission_classes = [IsAuthenticated]

    def _get_mapping(self, pk, user):
        try:
            return PatientDoctorMapping.objects.get(pk=pk, patient__created_by=user)
        except PatientDoctorMapping.DoesNotExist:
            return None

    def get(self, request, pk):
        mapping = self._get_mapping(pk, request.user)
        if not mapping:
            return Response(
                {"error": "Mapping not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PatientDoctorMappingSerializer(mapping)
        return Response(serializer.data)

    def delete(self, request, pk):
        mapping = self._get_mapping(pk, request.user)
        if not mapping:
            return Response(
                {"error": "Mapping not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        mapping.delete()
        return Response(
            {"message": "Mapping removed successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class PatientDoctorsView(APIView):
    """
    GET → List all doctors assigned to a specific patient.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        # Verify patient ownership
        if not Patient.objects.filter(pk=patient_id, created_by=request.user).exists():
            return Response(
                {"error": "Patient not found or does not belong to you"},
                status=status.HTTP_404_NOT_FOUND,
            )

        mappings = PatientDoctorMapping.objects.filter(patient_id=patient_id)
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)
