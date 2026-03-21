from django.db import IntegrityError
from django.test import TestCase

from staff.models import Trainer, SportDoctor
from users.models import CustomUser, UserRole


class TrainerModelTests(TestCase):
    """Tests for Trainer model."""

    def setUp(self) -> None:
        self.trainer: Trainer = Trainer.objects.create(
            first_name="Luca",
            last_name="Bianchi",
            fiscal_code="BNCLCU85B15H501X",
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.trainer), "Bianchi Luca (BNCLCU85B15H501X)")

    def test_repr(self) -> None:
        self.assertIn("Trainer(", repr(self.trainer))

    def test_fiscal_code_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            Trainer.objects.create(
                first_name="Clone",
                last_name="Clone",
                fiscal_code="BNCLCU85B15H501X",
            )

    def test_user_link_optional(self) -> None:
        self.assertIsNone(self.trainer.user)

    def test_user_link(self) -> None:
        user: CustomUser = CustomUser.objects.create_user(
            username="trainer",
            email="trainer@example.com",
            password="testpass123",
            role=UserRole.TRAINER,
        )
        self.trainer.user = user
        self.trainer.save()
        self.assertEqual(self.trainer.user, user)
        self.assertEqual(user.trainer_profile, self.trainer)

    def test_is_active_default_true(self) -> None:
        self.assertTrue(self.trainer.is_active)


class SportDoctorModelTests(TestCase):
    """Tests for SportDoctor model."""

    def setUp(self) -> None:
        self.doctor: SportDoctor = SportDoctor.objects.create(
            first_name="Giuseppe",
            last_name="Verdi",
            vat_number="12345678901",
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.doctor), "Verdi Giuseppe (P.IVA: 12345678901)")

    def test_repr(self) -> None:
        self.assertIn("SportDoctor(", repr(self.doctor))

    def test_vat_number_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            SportDoctor.objects.create(
                first_name="Clone",
                last_name="Clone",
                vat_number="12345678901",
            )

    def test_is_active_default_true(self) -> None:
        self.assertTrue(self.doctor.is_active)
