from django.apps import AppConfig


class ReceiptsConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "receipts"
    verbose_name: str = "Ricevute"
