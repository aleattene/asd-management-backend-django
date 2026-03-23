from rest_framework import serializers

from athletes.models import Athlete, Category
from geography.api.serializers import CountrySerializer


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

    nationality_detail = CountrySerializer(source="nationality", read_only=True)

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
            "nationality",
            "nationality_detail",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields: list[str] = ["id", "nationality_detail", "created_at", "updated_at"]
