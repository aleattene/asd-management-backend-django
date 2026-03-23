from rest_framework import serializers

from certificates.models import SportCertificate


class SportCertificateListSerializer(serializers.ModelSerializer):
    """Serializer for listing sport certificates (minimal fields)."""

    class Meta:
        model = SportCertificate
        fields: list[str] = [
            "id",
            "athlete",
            "doctor",
            "issue_date",
            "expiration_date",
            "is_active",
        ]


class SportCertificateDetailSerializer(serializers.ModelSerializer):
    """Serializer for sport certificate detail view."""

    def validate(self, data: dict) -> dict:
        """Validate that expiration_date is strictly after issue_date."""
        issue = data.get("issue_date", getattr(self.instance, "issue_date", None))
        expiration = data.get("expiration_date", getattr(self.instance, "expiration_date", None))
        if issue and expiration and expiration <= issue:
            raise serializers.ValidationError(
                {"expiration_date": "Expiration date must be after issue date."}
            )
        return data

    class Meta:
        model = SportCertificate
        fields: list[str] = [
            "id",
            "athlete",
            "doctor",
            "issue_date",
            "expiration_date",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields: list[str] = ["id", "created_at", "updated_at"]
