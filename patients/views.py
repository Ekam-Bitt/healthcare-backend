from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Patient
from .serializers import PatientSerializer


class PatientListCreateView(APIView):
    """
    GET  → List all patients belonging to the authenticated user.
    POST → Create a new patient under the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.filter(created_by=request.user)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetailView(APIView):
    """
    GET    → Retrieve a single patient.
    PUT    → Update a patient.
    DELETE → Delete a patient.
    """

    permission_classes = [IsAuthenticated]

    def _get_patient(self, pk, user):
        try:
            return Patient.objects.get(pk=pk, created_by=user)
        except Patient.DoesNotExist:
            return None

    def get(self, request, pk):
        patient = self._get_patient(pk, request.user)
        if not patient:
            return Response(
                {"error": "Patient not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def put(self, request, pk):
        patient = self._get_patient(pk, request.user)
        if not patient:
            return Response(
                {"error": "Patient not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        patient = self._get_patient(pk, request.user)
        if not patient:
            return Response(
                {"error": "Patient not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        patient.delete()
        return Response(
            {"message": "Patient deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
