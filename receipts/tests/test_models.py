from django.db.models.deletion import ProtectedError
from django.test import TestCase

from payment_methods.models import PaymentMethod
from receipts.models import Receipt
from users.models import CustomUser, UserRole


class ReceiptModelTests(TestCase):
    """Tests for Receipt model."""

    def setUp(self) -> None:
        self.user: CustomUser = CustomUser.objects.create_user(
            username="member",
            email="member@example.com",
            password="memberpass123",
            role=UserRole.MEMBER,
        )
        self.payment_method: PaymentMethod = PaymentMethod.objects.create(
            name="Contanti",
        )
        self.receipt: Receipt = Receipt.objects.create(
            date="2026-01-15",
            description="Quota iscrizione stagione 2025/2026",
            amount="150.00",
            user=self.user,
            payment_method=self.payment_method,
        )

    def test_str(self) -> None:
        self.assertIn("2026-01-15", str(self.receipt))
        self.assertIn("150", str(self.receipt))

    def test_repr(self) -> None:
        self.assertIn("Receipt(", repr(self.receipt))

    def test_user_protect_on_delete(self) -> None:
        with self.assertRaises(ProtectedError):
            self.user.delete()

    def test_payment_method_protect_on_delete(self) -> None:
        with self.assertRaises(ProtectedError):
            self.payment_method.delete()

    def test_is_active_default_true(self) -> None:
        self.assertTrue(self.receipt.is_active)

    def test_ordering(self) -> None:
        Receipt.objects.create(
            date="2026-03-01",
            description="Materiale sportivo",
            amount="50.00",
            user=self.user,
            payment_method=self.payment_method,
        )
        receipts: list = list(Receipt.objects.values_list("date", flat=True))
        self.assertGreater(receipts[0], receipts[1])
