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
        read_only_fields: list[str] = ["id", "role", "created_at", "updated_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user (admin/operator only).

    Role is intentionally excluded: new users are always created with the
    default role (member). Role changes require a dedicated superadmin endpoint.
    """

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
        ]

    def create(self, validated_data: dict) -> CustomUser:
        password: str = validated_data.pop("password")
        username: str = validated_data.pop("username")
        email: str = validated_data.pop("email")
        return CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            **validated_data,
        )


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
