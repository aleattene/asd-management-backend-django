from rest_framework import serializers

from staff.models import Trainer, SportDoctor


class TrainerSerializer(serializers.ModelSerializer):
    """Serializer for Trainer model."""

    class Meta:
        model = Trainer
        fields: list[str] = [
            "id",
            "user",
            "first_name",
            "last_name",
            "fiscal_code",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields: list[str] = ["id", "created_at", "updated_at"]


class SportDoctorSerializer(serializers.ModelSerializer):
    """Serializer for SportDoctor model."""

    class Meta:
        model = SportDoctor
        fields: list[str] = [
            "id",
            "first_name",
            "last_name",
            "vat_number",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields: list[str] = ["id", "created_at", "updated_at"]
