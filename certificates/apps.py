from django.apps import AppConfig


class CertificatesConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "certificates"
    verbose_name: str = "Certificazioni Medico-Sportive"
