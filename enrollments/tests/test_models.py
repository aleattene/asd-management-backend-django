import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from athletes.models import Athlete, Category
from enrollments.models import Enrollment
from users.models import CustomUser, UserRole


class EnrollmentModelTests(TestCase):
    """Tests for Enrollment model."""

    def setUp(self) -> None:
        self.guardian: CustomUser = CustomUser.objects.create_user(
            username="guardian",
            email="guardian@example.com",
            password="testpass123",
            role=UserRole.MEMBER,
        )
        self.category: Category = Category.objects.create(
            code="U14",
            description="Under 14",
            age_range="12-14",
        )
        self.athlete: Athlete = Athlete.objects.create(
            guardian=self.guardian,
            first_name="Luca",
            last_name="Rossi",
            fiscal_code="RSSLCU10A01H501Z",
            date_of_birth=datetime.date(2010, 1, 1),
            place_of_birth="Roma",
            category=self.category,
        )
        self.enrollment: Enrollment = Enrollment.objects.create(
            athlete=self.athlete,
            season="2025/2026",
            enrollment_date=datetime.date(2025, 9, 1),
        )

    def test_str(self) -> None:
        self.assertIn("2025/2026", str(self.enrollment))

    def test_repr(self) -> None:
        self.assertIn("Enrollment(", repr(self.enrollment))

    def test_is_active_default_true(self) -> None:
        self.assertTrue(self.enrollment.is_active)

    def test_guardian_signed_default_false(self) -> None:
        self.assertFalse(self.enrollment.guardian_signed)

    def test_unique_enrollment_per_season(self) -> None:
        with self.assertRaises(IntegrityError):
            Enrollment.objects.create(
                athlete=self.athlete,
                season="2025/2026",
                enrollment_date=datetime.date(2025, 9, 15),
            )

    def test_invalid_season_format(self) -> None:
        enrollment = Enrollment(
            athlete=self.athlete,
            season="25/26",
            enrollment_date=datetime.date(2025, 9, 1),
        )
        with self.assertRaises(ValidationError):
            enrollment.full_clean()

    def test_non_consecutive_season_years(self) -> None:
        enrollment = Enrollment(
            athlete=self.athlete,
            season="2025/2027",
            enrollment_date=datetime.date(2025, 9, 1),
        )
        with self.assertRaises(ValidationError):
            enrollment.full_clean()
