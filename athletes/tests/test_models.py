from django.db import IntegrityError
from django.test import TestCase

from athletes.models import Athlete, Category
from staff.models import Trainer
from users.models import CustomUser, UserRole


class CategoryModelTests(TestCase):
    """Tests for Category model."""

    def setUp(self) -> None:
        self.category: Category = Category.objects.create(
            code="U14",
            description="Under 14",
            age_range="12-13",
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.category), "U14 - Under 14")

    def test_repr(self) -> None:
        self.assertEqual(repr(self.category), "Category(code='U14', description='Under 14')")

    def test_code_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            Category.objects.create(code="U14", description="Duplicato")

    def test_is_active_default_true(self) -> None:
        self.assertTrue(self.category.is_active)


class AthleteModelTests(TestCase):
    """Tests for Athlete model."""

    def setUp(self) -> None:
        self.guardian: CustomUser = CustomUser.objects.create_user(
            username="genitore",
            email="genitore@example.com",
            password="testpass123",
            role=UserRole.MEMBER,
        )
        self.category: Category = Category.objects.create(
            code="U16", description="Under 16", age_range="14-15"
        )
        self.trainer: Trainer = Trainer.objects.create(
            first_name="Luca",
            last_name="Bianchi",
            fiscal_code="BNCLCU85B15H501X",
        )
        self.athlete: Athlete = Athlete.objects.create(
            guardian=self.guardian,
            first_name="Davide",
            last_name="Attene",
            fiscal_code="TTNDVD06P04H501A",
            date_of_birth="2006-09-04",
            place_of_birth="Roma",
            category=self.category,
            trainer=self.trainer,
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.athlete), "Attene Davide (TTNDVD06P04H501A)")

    def test_repr(self) -> None:
        self.assertIn("Athlete(", repr(self.athlete))

    def test_guardian_relationship(self) -> None:
        self.assertEqual(self.athlete.guardian, self.guardian)
        self.assertIn(self.athlete, self.guardian.athletes.all())

    def test_trainer_relationship(self) -> None:
        self.assertEqual(self.athlete.trainer, self.trainer)
        self.assertIn(self.athlete, self.trainer.athletes.all())

    def test_fiscal_code_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            Athlete.objects.create(
                guardian=self.guardian,
                first_name="Clone",
                last_name="Clone",
                fiscal_code="TTNDVD06P04H501A",
                date_of_birth="2006-01-01",
                place_of_birth="Milano",
                category=self.category,
            )

    def test_is_active_default_true(self) -> None:
        self.assertTrue(self.athlete.is_active)

    def test_trainer_nullable(self) -> None:
        athlete: Athlete = Athlete.objects.create(
            guardian=self.guardian,
            first_name="Senza",
            last_name="Allenatore",
            fiscal_code="SNZLLN00A01H501B",
            date_of_birth="2000-01-01",
            place_of_birth="Milano",
            category=self.category,
        )
        self.assertIsNone(athlete.trainer)
