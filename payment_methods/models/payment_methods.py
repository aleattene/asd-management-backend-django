from django.db import models


class PaymentMethod(models.Model):
    """Model representing a payment method (cash, bank transfer, etc.)."""

    name = models.CharField(max_length=50, unique=True, verbose_name="Nome")
    is_active = models.BooleanField(default=True, verbose_name="Attivo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Metodo di Pagamento"
        verbose_name_plural = "Metodi di Pagamento"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"PaymentMethod(name={self.name!r})"
