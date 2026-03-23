from rest_framework import serializers

from enrollments.models import Enrollment


class EnrollmentListSerializer(serializers.ModelSerializer):
    """Serializer for listing enrollments (minimal fields)."""

    class Meta:
        model = Enrollment
        fields: list[str] = ["id", "athlete", "season", "enrollment_date", "is_active"]


class EnrollmentDetailSerializer(serializers.ModelSerializer):
    """Serializer for enrollment detail view."""

    class Meta:
        model = Enrollment
        fields: list[str] = [
            "id",
            "athlete",
            "season",
            "enrollment_date",
            "guardian_signed",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields: list[str] = ["id", "created_at", "updated_at"]
