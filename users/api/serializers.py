from rest_framework import serializers

from users.models import CustomUser, UserRole


class _FiscalCodeNormalizeMixin:
    """Normalize fiscal_code: convert empty string to None before DB write."""

    def validate_fiscal_code(self, value: str) -> str | None:
        return value.strip() or None


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


class UserDetailSerializer(_FiscalCodeNormalizeMixin, serializers.ModelSerializer):
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
        extra_kwargs: dict = {"municipality": {"required": False}}


class UserCreateSerializer(_FiscalCodeNormalizeMixin, serializers.ModelSerializer):
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


class UserRoleSerializer(serializers.ModelSerializer):
    """Serializer for the superadmin-only role change endpoint."""

    role = serializers.ChoiceField(choices=UserRole.choices, required=True)

    class Meta:
        model = CustomUser
        fields: list[str] = ["id", "username", "role"]
        read_only_fields: list[str] = ["id", "username"]


class UserMeSerializer(_FiscalCodeNormalizeMixin, serializers.ModelSerializer):
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
