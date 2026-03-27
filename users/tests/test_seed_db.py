import os
from unittest import mock

from athletes.models import Athlete, Category
from certificates.models import SportCertificate
from companies.models import Company
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from doctors.models import SportDoctor
from enrollments.models import Enrollment
from invoices.models import Invoice
from payment_methods.models import PaymentMethod
from receipts.models import Receipt
from staff.models import Trainer

from users.models import CustomUser

SEED_ENV: dict[str, str] = {
    "SEED_SUPERADMIN_USERNAME": "test_superadmin",
    "SEED_SUPERADMIN_EMAIL": "superadmin@test.local",
    "SEED_SUPERADMIN_PASSWORD": "TestSuperadminPass1!",
    "SEED_ADMIN_USERNAME": "test_admin",
    "SEED_ADMIN_EMAIL": "admin@test.local",
    "SEED_ADMIN_PASSWORD": "TestAdminPass1!",
}


class SeedDbSmokeTests(TestCase):
    """Smoke tests for the seed_db management command.

    seed_db is called once for the whole class via setUpTestData to avoid
    repeating the full seeding (Faker-backed factories) for every test method.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        with override_settings(DEBUG=True):
            with mock.patch.dict(os.environ, SEED_ENV):
                call_command("seed_db")

    def test_seed_creates_payment_methods(self) -> None:
        self.assertEqual(PaymentMethod.objects.count(), 4)

    def test_seed_creates_categories(self) -> None:
        self.assertEqual(Category.objects.count(), 7)

    def test_seed_creates_users(self) -> None:
        # 2 admins + 3 operators + 4 trainers + 10 members + 3 externals + superadmin + admin
        self.assertEqual(CustomUser.objects.count(), 24)

    def test_seed_creates_superadmin(self) -> None:
        self.assertTrue(
            CustomUser.objects.filter(
                username=SEED_ENV["SEED_SUPERADMIN_USERNAME"], is_superuser=True
            ).exists()
        )

    def test_seed_creates_known_admin(self) -> None:
        self.assertTrue(
            CustomUser.objects.filter(username=SEED_ENV["SEED_ADMIN_USERNAME"]).exists()
        )

    def test_seed_creates_trainers(self) -> None:
        self.assertEqual(Trainer.objects.count(), 4)

    def test_seed_creates_doctors(self) -> None:
        self.assertEqual(SportDoctor.objects.count(), 3)

    def test_seed_creates_athletes(self) -> None:
        self.assertEqual(Athlete.objects.count(), 15)

    def test_seed_creates_enrollments(self) -> None:
        self.assertEqual(Enrollment.objects.count(), 15)

    def test_seed_creates_certificates(self) -> None:
        self.assertEqual(SportCertificate.objects.count(), 15)

    def test_seed_creates_companies(self) -> None:
        self.assertEqual(Company.objects.count(), 10)

    def test_seed_creates_invoices(self) -> None:
        self.assertEqual(Invoice.objects.count(), 20)

    def test_seed_creates_receipts(self) -> None:
        self.assertEqual(Receipt.objects.count(), 15)


@override_settings(DEBUG=True)
@mock.patch.dict(os.environ, SEED_ENV)
class SeedDbFlushTests(TestCase):
    """Tests for the --flush flag behaviour."""

    def test_flush_preserves_superusers(self) -> None:
        CustomUser.objects.create_superuser(
            username="su_test", email="su@test.local", password="pass"
        )
        call_command("seed_db", "--flush")
        self.assertTrue(CustomUser.objects.filter(username="su_test").exists())

    def test_flush_removes_non_superuser_data(self) -> None:
        call_command("seed_db")
        call_command("seed_db", "--flush")
        # After flush + re-seed counts must be correct (no duplicates)
        self.assertEqual(PaymentMethod.objects.count(), 4)
        self.assertEqual(Category.objects.count(), 7)

    def test_flush_then_reseed_no_integrity_error(self) -> None:
        call_command("seed_db")
        # Should not raise IntegrityError
        call_command("seed_db", "--flush")


class SeedDbGuardTests(TestCase):
    """Tests for environment guards."""

    @override_settings(DEBUG=False)
    def test_raises_error_when_debug_false(self) -> None:
        with self.assertRaises(CommandError):
            call_command("seed_db")

    @override_settings(DEBUG=True)
    def test_raises_error_when_seed_env_vars_missing(self) -> None:
        env_without_seed = {k: v for k, v in os.environ.items() if not k.startswith("SEED_")}
        with mock.patch.dict(os.environ, env_without_seed, clear=True):
            with self.assertRaises(CommandError):
                call_command("seed_db")
