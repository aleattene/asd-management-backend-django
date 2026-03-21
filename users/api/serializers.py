from rest_framework import serializers

from users.models import CustomUser


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users (minimal fields)."""

    class Meta:
        model = CustomUser
        fields: list[str] = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_active",
            "is_authorized",
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for user detail view."""

    class Meta:
        model = CustomUser
        fields: list[str] = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "fiscal_code",
            "phone_number",
            "date_of_birth",
            "role",
            "address_street",
            "address_number",
            "address_zip",
            "municipality",
            "is_active",
            "is_authorized",
            "created_at",
            "updated_at",
        ]
        read_only_fields: list[str] = ["id", "created_at", "updated_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user (admin/operator only)."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields: list[str] = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "fiscal_code",
            "phone_number",
            "date_of_birth",
            "role",
        ]

    def create(self, validated_data: dict) -> CustomUser:
        password: str = validated_data.pop("password")
        user: CustomUser = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserMeSerializer(serializers.ModelSerializer):
    """Serializer for the authenticated user's own profile."""

    class Meta:
        model = CustomUser
        fields: list[str] = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "fiscal_code",
            "phone_number",
            "date_of_birth",
            "role",
            "address_street",
            "address_number",
            "address_zip",
            "municipality",
            "is_authorized",
            "created_at",
            "updated_at",
        ]
        read_only_fields: list[str] = [
            "id",
            "username",
            "role",
            "is_authorized",
            "created_at",
            "updated_at",
        ]
