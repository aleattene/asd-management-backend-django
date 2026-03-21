from django.db import models


class SportDoctor(models.Model):
    """Model representing a sport doctor."""

    first_name = models.CharField(max_length=100, verbose_name="Nome")
    last_name = models.CharField(max_length=100, verbose_name="Cognome")
    vat_number = models.CharField(
        max_length=11, unique=True, verbose_name="Partita IVA"
    )
    is_active = models.BooleanField(default=True, verbose_name="Attivo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Medico Sportivo"
        verbose_name_plural = "Medici Sportivi"
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} (P.IVA: {self.vat_number})"

    def __repr__(self) -> str:
        return (
            f"SportDoctor(first_name={self.first_name!r}, last_name={self.last_name!r}, "
            f"vat_number={self.vat_number!r})"
        )
