from django.db import models


class InvoiceDirection(models.TextChoices):
    PURCHASE = "purchase", "Acquisto"
    SALE = "sale", "Vendita"


class Invoice(models.Model):
    """Model representing an invoice (purchase or sale)."""

    date = models.DateField(verbose_name="Data Fattura")
    number = models.CharField(max_length=25, verbose_name="Numero Fattura")
    description = models.CharField(max_length=200, verbose_name="Descrizione")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Importo"
    )
    direction = models.CharField(
        max_length=8,
        choices=InvoiceDirection.choices,
        verbose_name="Tipo",
    )
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.PROTECT,
        related_name="invoices",
        verbose_name="Società",
    )
    payment_method = models.ForeignKey(
        "payment_methods.PaymentMethod",
        on_delete=models.PROTECT,
        related_name="invoices",
        verbose_name="Metodo di Pagamento",
    )
    is_active = models.BooleanField(default=True, verbose_name="Attivo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fattura"
        verbose_name_plural = "Fatture"
        ordering = ["-date", "number"]

    def __str__(self) -> str:
        return f"Fattura {self.number} — {self.company} ({self.get_direction_display()})"

    def __repr__(self) -> str:
        return (
            f"Invoice(number={self.number!r}, company_id={self.company_id}, "
            f"direction={self.direction!r}, amount={self.amount!r})"
        )
