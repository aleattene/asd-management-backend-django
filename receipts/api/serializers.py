from rest_framework import serializers

from receipts.models import Receipt


class ReceiptListSerializer(serializers.ModelSerializer):
    """Serializer for listing receipts (minimal fields)."""

    class Meta:
        model = Receipt
        fields: list[str] = [
            "id",
            "date",
            "description",
            "amount",
            "user",
            "payment_method",
            "is_active",
        ]


class ReceiptDetailSerializer(serializers.ModelSerializer):
    """Serializer for receipt detail view."""

    class Meta:
        model = Receipt
        fields: list[str] = [
            "id",
            "date",
            "description",
            "amount",
            "user",
            "payment_method",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields: list[str] = ["id", "created_at", "updated_at"]
