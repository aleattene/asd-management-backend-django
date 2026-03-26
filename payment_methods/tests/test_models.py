from django.db import IntegrityError
from django.test import TestCase

from payment_methods.models import PaymentMethod


class PaymentMethodModelTests(TestCase):
    """Tests for PaymentMethod model."""

    def setUp(self) -> None:
        self.payment_method: PaymentMethod = PaymentMethod.objects.create(
            name="Contanti",
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.payment_method), "Contanti")

    def test_repr(self) -> None:
        self.assertIn("PaymentMethod(", repr(self.payment_method))

    def test_name_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            PaymentMethod.objects.create(name="Contanti")

    def test_is_active_default_true(self) -> None:
        self.assertTrue(self.payment_method.is_active)

    def test_ordering(self) -> None:
        PaymentMethod.objects.create(name="Bonifico")
        PaymentMethod.objects.create(name="Carta di credito")
        methods: list = list(PaymentMethod.objects.values_list("name", flat=True))
        self.assertEqual(methods[0], "Bonifico")
        self.assertEqual(methods[1], "Carta di credito")
        self.assertEqual(methods[2], "Contanti")
