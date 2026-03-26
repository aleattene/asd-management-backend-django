from django.apps import AppConfig


class CompaniesConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "companies"
    verbose_name: str = "Società Partner"
