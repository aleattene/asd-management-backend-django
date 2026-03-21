from django.apps import AppConfig


class AthletesConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "athletes"
    verbose_name: str = "Gestione Atleti"
