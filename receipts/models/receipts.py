from django.conf import settings
from django.db import models


class Receipt(models.Model):
    """Model representing a receipt issued by or to the ASD."""

    date = models.DateField(verbose_name="Data Ricevuta")
    description = models.CharField(max_length=200, verbose_name="Descrizione")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Importo"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="receipts",
        verbose_name="Utente",
    )
    payment_method = models.ForeignKey(
        "payment_methods.PaymentMethod",
        on_delete=models.PROTECT,
        related_name="receipts",
        verbose_name="Metodo di Pagamento",
    )
    is_active = models.BooleanField(default=True, verbose_name="Attivo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ricevuta"
        verbose_name_plural = "Ricevute"
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"Ricevuta {self.date} — {self.user} ({self.amount})"

    def __repr__(self) -> str:
        return (
            f"Receipt(date={self.date!r}, user_id={self.user_id}, "
            f"amount={self.amount!r})"
        )
