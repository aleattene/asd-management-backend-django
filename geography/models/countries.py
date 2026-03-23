from django.db import models


class Country(models.Model):
    """Model representing a country. Used as nationality reference for athletes."""

    name = models.CharField(max_length=100, verbose_name="Nome")
    iso_code = models.CharField(
        max_length=3,
        unique=True,
        blank=True,
        default="",
        verbose_name="Codice ISO",
    )
    is_active = models.BooleanField(default=True, verbose_name="Attivo")

    class Meta:
        verbose_name = "Nazione"
        verbose_name_plural = "Nazioni"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Country(name={self.name!r}, iso_code={self.iso_code!r})"
