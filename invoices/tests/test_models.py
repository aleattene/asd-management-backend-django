from django.db.models.deletion import ProtectedError
from django.test import TestCase

from companies.models import Company
from invoices.models import Invoice, InvoiceDirection
from payment_methods.models import PaymentMethod


class InvoiceModelTests(TestCase):
    """Tests for Invoice model."""

    def setUp(self) -> None:
        self.company: Company = Company.objects.create(
            business_name="Fornitore S.r.l.",
            vat_number="12345678901",
        )
        self.payment_method: PaymentMethod = PaymentMethod.objects.create(
            name="Bonifico",
        )
        self.invoice: Invoice = Invoice.objects.create(
            date="2026-01-15",
            number="2026/001",
            description="Materiale sportivo",
            amount="1500.00",
            direction=InvoiceDirection.PURCHASE,
            company=self.company,
            payment_method=self.payment_method,
        )

    def test_str(self) -> None:
        self.assertIn("2026/001", str(self.invoice))
        self.assertIn("Fornitore S.r.l.", str(self.invoice))

    def test_repr(self) -> None:
        self.assertIn("Invoice(", repr(self.invoice))

    def test_direction_purchase(self) -> None:
        self.assertEqual(self.invoice.direction, InvoiceDirection.PURCHASE)
        self.assertEqual(self.invoice.get_direction_display(), "Acquisto")

    def test_direction_sale(self) -> None:
        invoice: Invoice = Invoice.objects.create(
            date="2026-02-01",
            number="2026/V001",
            description="Vendita attrezzatura",
            amount="500.00",
            direction=InvoiceDirection.SALE,
            company=self.company,
            payment_method=self.payment_method,
        )
        self.assertEqual(invoice.get_direction_display(), "Vendita")

    def test_company_protect_on_delete(self) -> None:
        with self.assertRaises(ProtectedError):
            self.company.delete()

    def test_payment_method_protect_on_delete(self) -> None:
        with self.assertRaises(ProtectedError):
            self.payment_method.delete()

    def test_is_active_default_true(self) -> None:
        self.assertTrue(self.invoice.is_active)

    def test_ordering(self) -> None:
        Invoice.objects.create(
            date="2026-03-01",
            number="2026/002",
            description="Altro acquisto",
            amount="200.00",
            direction=InvoiceDirection.PURCHASE,
            company=self.company,
            payment_method=self.payment_method,
        )
        invoices: list = list(Invoice.objects.values_list("number", flat=True))
        self.assertEqual(invoices[0], "2026/002")
        self.assertEqual(invoices[1], "2026/001")
