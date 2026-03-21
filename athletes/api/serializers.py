from rest_framework import serializers

from athletes.models import Athlete, Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = Category
        fields: list[str] = ["id", "code", "description", "age_range", "is_active"]


class AthleteListSerializer(serializers.ModelSerializer):
    """Serializer for listing athletes (minimal fields)."""

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Athlete
        fields: list[str] = [
            "id",
            "first_name",
            "last_name",
            "fiscal_code",
            "category",
            "is_active",
        ]


class AthleteDetailSerializer(serializers.ModelSerializer):
    """Serializer for athlete detail view."""

    class Meta:
        model = Athlete
        fields: list[str] = [
            "id",
            "guardian",
            "first_name",
            "last_name",
            "fiscal_code",
            "date_of_birth",
            "place_of_birth",
            "category",
            "trainer",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields: list[str] = ["id", "created_at", "updated_at"]
