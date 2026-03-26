from django.apps import AppConfig


class PaymentMethodsConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "payment_methods"
    verbose_name: str = "Metodi di Pagamento"
