from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorListCreateView(APIView):
    """
    GET  → List all doctors.
    POST → Create a new doctor.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetailView(APIView):
    """
    GET    → Retrieve a single doctor.
    PUT    → Update a doctor.
    DELETE → Delete a doctor.
    """

    permission_classes = [IsAuthenticated]

    def _get_doctor(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return None

    def get(self, request, pk):
        doctor = self._get_doctor(pk)
        if not doctor:
            return Response(
                {"error": "Doctor not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    def put(self, request, pk):
        doctor = self._get_doctor(pk)
        if not doctor:
            return Response(
                {"error": "Doctor not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        doctor = self._get_doctor(pk)
        if not doctor:
            return Response(
                {"error": "Doctor not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        doctor.delete()
        return Response(
            {"message": "Doctor deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
