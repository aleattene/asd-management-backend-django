from django.db import IntegrityError
from django.test import TestCase

from companies.models import Company


class CompanyModelTests(TestCase):
    """Tests for Company model."""

    def setUp(self) -> None:
        self.company: Company = Company.objects.create(
            business_name="Palestra Sport S.r.l.",
            vat_number="12345678901",
            fiscal_code="12345678901",
            vat_equals_fc=True,
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.company), "Palestra Sport S.r.l.")

    def test_repr(self) -> None:
        self.assertIn("Company(", repr(self.company))

    def test_vat_number_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            Company.objects.create(
                business_name="Altra Palestra S.r.l.",
                vat_number="12345678901",
            )

    def test_fiscal_code_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            Company.objects.create(
                business_name="Altra Palestra S.r.l.",
                fiscal_code="12345678901",
            )

    def test_vat_number_nullable(self) -> None:
        company: Company = Company.objects.create(
            business_name="Privato Rossi",
            fiscal_code="RSSMRA80A01H501Z",
        )
        self.assertIsNone(company.vat_number)

    def test_fiscal_code_nullable(self) -> None:
        company: Company = Company.objects.create(
            business_name="Ditta Estera",
            vat_number="98765432101",
        )
        self.assertIsNone(company.fiscal_code)

    def test_is_active_default_true(self) -> None:
        self.assertTrue(self.company.is_active)

    def test_vat_equals_fc_default_false(self) -> None:
        company: Company = Company.objects.create(
            business_name="Test Default S.r.l.",
        )
        self.assertFalse(company.vat_equals_fc)

    def test_ordering(self) -> None:
        Company.objects.create(business_name="AAA First S.r.l.")
        Company.objects.create(business_name="ZZZ Last S.r.l.")
        companies: list = list(Company.objects.values_list("business_name", flat=True))
        self.assertEqual(companies[0], "AAA First S.r.l.")
