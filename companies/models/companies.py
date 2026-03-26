from django.db import models


class Company(models.Model):
    """Model representing an external company (client, supplier, partner)."""

    business_name = models.CharField(max_length=150, verbose_name="Ragione Sociale")
    vat_number = models.CharField(
        max_length=11,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Partita IVA",
    )
    fiscal_code = models.CharField(
        max_length=16,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Codice Fiscale",
    )
    vat_equals_fc = models.BooleanField(
        default=False,
        verbose_name="P.IVA coincide con CF",
    )
    is_active = models.BooleanField(default=True, verbose_name="Attivo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Società"
        verbose_name_plural = "Società"
        ordering = ["business_name"]

    def __str__(self) -> str:
        return self.business_name

    def __repr__(self) -> str:
        return f"Company(business_name={self.business_name!r}, vat_number={self.vat_number!r})"
