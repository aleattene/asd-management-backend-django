from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser."""

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_authorized",
        "is_active",
    )
    list_filter = ("role", "is_authorized", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name", "fiscal_code")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Informazioni aggiuntive",
            {
                "fields": (
                    "role",
                    "fiscal_code",
                    "phone_number",
                    "date_of_birth",
                    "is_authorized",
                ),
            },
        ),
        (
            "Indirizzo",
            {
                "fields": (
                    "address_street",
                    "address_number",
                    "address_zip",
                    "municipality",
                ),
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Informazioni aggiuntive",
            {
                "fields": ("email", "role", "fiscal_code", "phone_number"),
            },
        ),
    )
