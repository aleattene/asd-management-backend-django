from django.conf import settings
from django.db import models


class Athlete(models.Model):
    """Model representing an athlete registered in the ASD."""

    guardian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="athletes",
        verbose_name="Responsabile",
    )
    first_name = models.CharField(max_length=100, verbose_name="Nome")
    last_name = models.CharField(max_length=100, verbose_name="Cognome")
    fiscal_code = models.CharField(
        max_length=16, unique=True, verbose_name="Codice Fiscale"
    )
    date_of_birth = models.DateField(verbose_name="Data di Nascita")
    place_of_birth = models.CharField(max_length=150, verbose_name="Luogo di Nascita")
    category = models.ForeignKey(
        "athletes.Category",
        on_delete=models.PROTECT,
        related_name="athletes",
        verbose_name="Categoria",
    )
    trainer = models.ForeignKey(
        "staff.Trainer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="athletes",
        verbose_name="Allenatore",
    )
    is_active = models.BooleanField(default=True, verbose_name="Attivo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Atleta"
        verbose_name_plural = "Atleti"
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} ({self.fiscal_code})"

    def __repr__(self) -> str:
        return (
            f"Athlete(first_name={self.first_name!r}, last_name={self.last_name!r}, "
            f"fiscal_code={self.fiscal_code!r})"
        )
