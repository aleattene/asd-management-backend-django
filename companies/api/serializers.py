from rest_framework import serializers

from companies.models import Company


class _NullableFieldNormalizeMixin:
    """Normalize unique nullable fields: convert empty string to None before DB write."""

    def validate_vat_number(self, value: str) -> str | None:
        return value.strip() or None if value else None

    def validate_fiscal_code(self, value: str) -> str | None:
        return value.strip() or None if value else None


class CompanySerializer(_NullableFieldNormalizeMixin, serializers.ModelSerializer):
    """Serializer for Company model."""

    class Meta:
        model = Company
        fields: list[str] = [
            "id",
            "business_name",
            "vat_number",
            "fiscal_code",
            "vat_equals_fc",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields: list[str] = ["id", "created_at", "updated_at"]
