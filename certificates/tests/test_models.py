import datetime

from django.test import TestCase

from athletes.models import Athlete, Category
from certificates.models import SportCertificate
from doctors.models import SportDoctor
from users.models import CustomUser, UserRole


class SportCertificateModelTests(TestCase):
    """Tests for SportCertificate model."""

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
        self.doctor: SportDoctor = SportDoctor.objects.create(
            first_name="Giuseppe",
            last_name="Verdi",
            vat_number="12345678901",
        )
        self.certificate: SportCertificate = SportCertificate.objects.create(
            athlete=self.athlete,
            doctor=self.doctor,
            issue_date=datetime.date(2025, 9, 1),
            expiration_date=datetime.date(2026, 9, 1),
        )

    def test_str(self) -> None:
        self.assertIn("2026-09-01", str(self.certificate))

    def test_repr(self) -> None:
        self.assertIn("SportCertificate(", repr(self.certificate))

    def test_is_active_default_true(self) -> None:
        self.assertTrue(self.certificate.is_active)

    def test_doctor_fk(self) -> None:
        self.assertEqual(self.certificate.doctor, self.doctor)

    def test_athlete_fk(self) -> None:
        self.assertEqual(self.certificate.athlete, self.athlete)
