from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    PatientListCreate,
    PatientDetail,
    DoctorListCreate,
    DoctorDetail,
    MappingListCreate,
    MappingDelete,
    MappingByPatient,
)

urlpatterns = [
    # Auth
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Patients
    path("patients/", PatientListCreate.as_view()),
    path("patients/<int:pk>/", PatientDetail.as_view()),
    # Doctors
    path("doctors/", DoctorListCreate.as_view()),
    path("doctors/<int:pk>/", DoctorDetail.as_view()),
    # Mappings
    path("mappings/", MappingListCreate.as_view()),
    path("mappings/<int:pk>/", MappingDelete.as_view()),
    path("mappings/patient/<int:patient_id>/", MappingByPatient.as_view()),
]
