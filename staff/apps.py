from django.apps import AppConfig


class StaffConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "staff"
    verbose_name: str = "Gestione Staff"
