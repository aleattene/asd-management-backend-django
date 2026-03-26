from pathlib import Path
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from geography.models import Country, Municipality, Province

TEST_DATA_DIR: Path = Path(__file__).resolve().parent / "data"
PATCH_TARGET: str = "geography.management.commands.import_geography.DATA_DIR"


class ImportCountriesTests(TestCase):
    """Tests for import_geography --countries."""

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_countries_creates_records(self) -> None:
        call_command("import_geography", "--countries")
        self.assertEqual(Country.objects.count(), 5)

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_countries_idempotent(self) -> None:
        call_command("import_geography", "--countries")
        call_command("import_geography", "--countries")
        self.assertEqual(Country.objects.count(), 5)

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_countries_updates_name(self) -> None:
        Country.objects.create(iso_code="ITA", name="Old Name")
        call_command("import_geography", "--countries")
        country: Country = Country.objects.get(iso_code="ITA")
        self.assertEqual(country.name, "Italia")

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_countries_dry_run(self) -> None:
        call_command("import_geography", "--countries", "--dry-run")
        self.assertEqual(Country.objects.count(), 0)

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_countries_sets_is_active(self) -> None:
        call_command("import_geography", "--countries")
        self.assertTrue(Country.objects.get(iso_code="ITA").is_active)


class ImportProvincesTests(TestCase):
    """Tests for import_geography --provinces."""

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_provinces_creates_records(self) -> None:
        call_command("import_geography", "--provinces")
        self.assertEqual(Province.objects.count(), 5)

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_provinces_idempotent(self) -> None:
        call_command("import_geography", "--provinces")
        call_command("import_geography", "--provinces")
        self.assertEqual(Province.objects.count(), 5)

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_provinces_updates_name(self) -> None:
        Province.objects.create(code="RM", name="Old Rome")
        call_command("import_geography", "--provinces")
        province: Province = Province.objects.get(code="RM")
        self.assertEqual(province.name, "Roma")

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_provinces_dry_run(self) -> None:
        call_command("import_geography", "--provinces", "--dry-run")
        self.assertEqual(Province.objects.count(), 0)


class ImportMunicipalitiesTests(TestCase):
    """Tests for import_geography --municipalities."""

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_municipalities_creates_records(self) -> None:
        call_command("import_geography", "--provinces")
        call_command("import_geography", "--municipalities")
        # 7 valid rows (Comune Ignoto with province XX is skipped)
        self.assertEqual(Municipality.objects.count(), 7)

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_municipalities_skips_unknown_province(self) -> None:
        call_command("import_geography", "--provinces")
        call_command("import_geography", "--municipalities")
        # "Comune Ignoto" with province_code "XX" should be skipped
        self.assertFalse(Municipality.objects.filter(name="Comune Ignoto").exists())

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_municipalities_idempotent(self) -> None:
        call_command("import_geography", "--provinces")
        call_command("import_geography", "--municipalities")
        call_command("import_geography", "--municipalities")
        self.assertEqual(Municipality.objects.count(), 7)

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_municipalities_dry_run(self) -> None:
        call_command("import_geography", "--provinces")
        call_command("import_geography", "--municipalities", "--dry-run")
        self.assertEqual(Municipality.objects.count(), 0)

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_municipalities_requires_provinces(self) -> None:
        # No provinces in DB — should print error and skip
        call_command("import_geography", "--municipalities")
        self.assertEqual(Municipality.objects.count(), 0)

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_municipalities_fk_correct(self) -> None:
        call_command("import_geography", "--provinces")
        call_command("import_geography", "--municipalities")
        roma: Municipality = Municipality.objects.get(name="Roma")
        self.assertEqual(roma.province.code, "RM")


class ImportAllTests(TestCase):
    """Tests for import_geography with no flags (default = all)."""

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_all_default(self) -> None:
        call_command("import_geography")
        self.assertEqual(Country.objects.count(), 5)
        self.assertEqual(Province.objects.count(), 5)
        self.assertEqual(Municipality.objects.count(), 7)

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_import_all_flag(self) -> None:
        call_command("import_geography", "--all")
        self.assertEqual(Country.objects.count(), 5)
        self.assertEqual(Province.objects.count(), 5)
        self.assertEqual(Municipality.objects.count(), 7)


class ImportEdgeCaseTests(TestCase):
    """Tests for edge cases."""

    def test_missing_csv_raises_error(self) -> None:
        # Use a guaranteed-missing path inside the test data directory
        fake_dir: Path = TEST_DATA_DIR / "_nonexistent_subdir_for_test"
        with patch(PATCH_TARGET, fake_dir):
            with self.assertRaises(CommandError):
                call_command("import_geography", "--countries")

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_municipalities_without_provinces_returns_error_message(self) -> None:
        from io import StringIO
        stdout = StringIO()
        call_command("import_geography", "--municipalities", stdout=stdout)
        self.assertEqual(Municipality.objects.count(), 0)
        self.assertIn("No provinces in DB", stdout.getvalue())

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_dry_run_all_does_not_require_db_provinces(self) -> None:
        """--dry-run with default/all flags must not fail due to missing DB provinces."""
        call_command("import_geography", "--dry-run")
        self.assertEqual(Country.objects.count(), 0)
        self.assertEqual(Province.objects.count(), 0)
        self.assertEqual(Municipality.objects.count(), 0)

    @patch(PATCH_TARGET, TEST_DATA_DIR)
    def test_dry_run_municipalities_standalone(self) -> None:
        """--municipalities --dry-run must work without provinces in DB."""
        call_command("import_geography", "--municipalities", "--dry-run")
        self.assertEqual(Municipality.objects.count(), 0)
