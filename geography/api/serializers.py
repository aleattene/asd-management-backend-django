from rest_framework import serializers

from geography.models import Country, Province, Municipality


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country model."""

    class Meta:
        model = Country
        fields: list[str] = ["id", "name", "iso_code", "is_active"]


class ProvinceSerializer(serializers.ModelSerializer):
    """Serializer for Province model."""

    class Meta:
        model = Province
        fields: list[str] = ["id", "name", "code"]


class MunicipalitySerializer(serializers.ModelSerializer):
    """Serializer for Municipality model."""

    province_detail = ProvinceSerializer(source="province", read_only=True)

    class Meta:
        model = Municipality
        fields: list[str] = ["id", "name", "province", "province_detail"]
