from rest_framework import serializers

from invoices.models import Invoice


class InvoiceListSerializer(serializers.ModelSerializer):
    """Serializer for listing invoices (minimal fields)."""

    class Meta:
        model = Invoice
        fields: list[str] = [
            "id",
            "date",
            "number",
            "description",
            "amount",
            "direction",
            "company",
            "payment_method",
            "is_active",
        ]


class InvoiceDetailSerializer(serializers.ModelSerializer):
    """Serializer for invoice detail view."""

    class Meta:
        model = Invoice
        fields: list[str] = [
            "id",
            "date",
            "number",
            "description",
            "amount",
            "direction",
            "company",
            "payment_method",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields: list[str] = ["id", "created_at", "updated_at"]
