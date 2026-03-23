from django.db import models


class Municipality(models.Model):
    """Model representing an Italian municipality (comune)."""

    name = models.CharField(max_length=150, verbose_name="Denominazione")
    province = models.ForeignKey(
        "geography.Province",
        on_delete=models.PROTECT,
        related_name="municipalities",
        verbose_name="Provincia",
    )

    class Meta:
        verbose_name = "Comune"
        verbose_name_plural = "Comuni"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.province.code})"

    def __repr__(self) -> str:
        return f"Municipality(name={self.name!r}, province={self.province.code!r})"
