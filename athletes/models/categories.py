from django.db import models


class Category(models.Model):
    """Model representing an athlete age category."""

    code = models.CharField(max_length=10, unique=True, verbose_name="Codice")
    description = models.CharField(max_length=100, verbose_name="Descrizione")
    age_range = models.CharField(
        max_length=20, blank=True, default="", verbose_name="Fascia di Eta'"
    )
    is_active = models.BooleanField(default=True, verbose_name="Attiva")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorie"
        ordering = ["code"]

    def __str__(self) -> str:
        return f"{self.code} - {self.description}"

    def __repr__(self) -> str:
        return f"Category(code={self.code!r}, description={self.description!r})"
