from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient, Doctor, PatientDoctorMapping


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class PatientSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
        read_only_fields = ["user"]


class MappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source="patient.name")
    doctor_name = serializers.ReadOnlyField(source="doctor.name")
    patient_id = serializers.IntegerField(source="patient.id", read_only=True)
    doctor_id = serializers.IntegerField(source="doctor.id", read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            "id",
            "patient_id",
            "patient_name",
            "doctor_id",
            "doctor_name",
            "assigned_date",
        ]
        read_only_fields = ["assigned_date"]
