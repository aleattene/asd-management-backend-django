from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from geography.models import Country, Province, Municipality


class CountryModelTests(TestCase):
    """Tests for Country model."""

    def setUp(self) -> None:
        self.country: Country = Country.objects.create(
            name="Italia", iso_code="ITA"
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.country), "Italia")

    def test_repr(self) -> None:
        self.assertIn("Country(", repr(self.country))

    def test_iso_code_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            Country.objects.create(name="Italy Duplicate", iso_code="ITA")

    def test_is_active_default_true(self) -> None:
        self.assertTrue(self.country.is_active)


class ProvinceModelTests(TestCase):
    """Tests for Province model."""

    def setUp(self) -> None:
        self.province: Province = Province.objects.create(
            name="Roma", code="RM"
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.province), "Roma (RM)")

    def test_repr(self) -> None:
        self.assertIn("Province(", repr(self.province))

    def test_code_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            Province.objects.create(name="Roma Duplicate", code="RM")


class MunicipalityModelTests(TestCase):
    """Tests for Municipality model."""

    def setUp(self) -> None:
        self.province: Province = Province.objects.create(
            name="Roma", code="RM"
        )
        self.municipality: Municipality = Municipality.objects.create(
            name="Roma", province=self.province
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.municipality), "Roma (RM)")

    def test_repr(self) -> None:
        self.assertIn("Municipality(", repr(self.municipality))

    def test_province_fk(self) -> None:
        self.assertEqual(self.municipality.province, self.province)

    def test_province_protect_on_delete(self) -> None:
        with self.assertRaises(ProtectedError):
            self.province.delete()

    def test_unique_name_per_province(self) -> None:
        with self.assertRaises(IntegrityError):
            Municipality.objects.create(name="Roma", province=self.province)

    def test_same_name_different_province_allowed(self) -> None:
        other_province: Province = Province.objects.create(name="Milano", code="MI")
        duplicate: Municipality = Municipality.objects.create(
            name="Roma", province=other_province
        )
        self.assertEqual(duplicate.province.code, "MI")
