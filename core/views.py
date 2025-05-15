from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserSerializer,
    PatientSerializer,
    DoctorSerializer,
    MappingSerializer,
)


# used for register and login user
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)


# Create and Retrieve Patients
class PatientListCreate(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Retrieve, update, delete a patient
class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)


# Create and retrieve doctors
class DoctorListCreate(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Retrieve, update, delete a doctor
class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this doctor")
        return obj


# Create and retrieve mapping between patients & doctors
class MappingListCreate(generics.ListCreateAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        patient_id = request.data.get("patient")
        doctor_id = request.data.get("doctor")

        # check if inputs are provided
        if not patient_id or not doctor_id:
            return Response(
                {"error": "Both patient id and doctor id fields are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if patient belongs to current user
        patient = Patient.objects.filter(id=patient_id, user=request.user).first()
        if not patient:
            return Response(
                {"error": "Patient not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if doctor belongs to current user
        doctor = Doctor.objects.filter(id=doctor_id, user=request.user).first()
        if not doctor:
            return Response(
                {"error": "Doctor not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Avoid duplicate mappings
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            return Response(
                {"error": "This mapping already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save mapping
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Delete Mappings
class MappingDelete(generics.DestroyAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        mapping = get_object_or_404(PatientDoctorMapping, pk=kwargs["pk"])

        # Check access before deletions
        if mapping.patient.user != request.user or mapping.doctor.user != request.user:
            raise PermissionDenied("You cannot delete this mapping")

        return super().destroy(request, *args, **kwargs)


# retrive mapping for perticualr patient based on <patient_id>
class MappingByPatient(generics.ListAPIView):
    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs.get("patient_id")

        # Ensure the patient exists and belongs to the current user
        try:
            patient = Patient.objects.get(id=patient_id, user=self.request.user)
        except Patient.DoesNotExist:
            raise NotFound("Patient not found or access denied")

        return PatientDoctorMapping.objects.filter(patient=patient)
