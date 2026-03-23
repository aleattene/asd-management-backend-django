from django.db import models


class Province(models.Model):
    """Model representing an Italian province."""

    name = models.CharField(max_length=100, verbose_name="Denominazione")
    code = models.CharField(max_length=2, unique=True, verbose_name="Sigla")

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Province"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

    def __repr__(self) -> str:
        return f"Province(name={self.name!r}, code={self.code!r})"
