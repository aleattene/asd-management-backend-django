from django.conf import settings
from django.db import models


class Trainer(models.Model):
    """Model representing a trainer/coach."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trainer_profile",
        verbose_name="Account Utente",
    )
    first_name = models.CharField(max_length=100, verbose_name="Nome")
    last_name = models.CharField(max_length=100, verbose_name="Cognome")
    fiscal_code = models.CharField(
        max_length=16, unique=True, verbose_name="Codice Fiscale"
    )
    is_active = models.BooleanField(default=True, verbose_name="Attivo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Allenatore"
        verbose_name_plural = "Allenatori"
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} ({self.fiscal_code})"

    def __repr__(self) -> str:
        return (
            f"Trainer(first_name={self.first_name!r}, last_name={self.last_name!r}, "
            f"fiscal_code={self.fiscal_code!r})"
        )
