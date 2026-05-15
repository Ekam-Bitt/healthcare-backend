from django.urls import path

from .views import MappingDetailView, MappingListCreateView, PatientDoctorsView

urlpatterns = [
    path("", MappingListCreateView.as_view(), name="mapping-list-create"),
    path("<int:pk>/", MappingDetailView.as_view(), name="mapping-detail"),
    # Assignment spec: GET /api/mappings/<patient_id>/ → doctors for a patient
    path("<int:patient_id>/doctors/", PatientDoctorsView.as_view(), name="patient-doctors"),
]
