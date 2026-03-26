from django.apps import AppConfig


class InvoicesConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "invoices"
    verbose_name: str = "Fatture"
