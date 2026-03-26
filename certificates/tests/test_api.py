import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from athletes.models import Athlete, Category
from certificates.models import SportCertificate
from doctors.models import SportDoctor
from staff.models import Trainer
from users.models import CustomUser, UserRole


class CertificateSetupMixin:
    """Shared setup for certificate API tests."""

    def setUp(self) -> None:
        self.client: APIClient = APIClient()

        self.admin: CustomUser = CustomUser.objects.create_user(
            username="admin", email="admin@example.com",
            password="adminpass123", role=UserRole.ADMIN,
        )
        self.operator: CustomUser = CustomUser.objects.create_user(
            username="operator", email="operator@example.com",
            password="operatorpass123", role=UserRole.OPERATOR,
        )
        self.guardian: CustomUser = CustomUser.objects.create_user(
            username="guardian", email="guardian@example.com",
            password="guardianpass123", role=UserRole.MEMBER,
        )
        self.other_guardian: CustomUser = CustomUser.objects.create_user(
            username="other", email="other@example.com",
            password="otherpass123", role=UserRole.MEMBER,
        )
        self.trainer_user: CustomUser = CustomUser.objects.create_user(
            username="trainer", email="trainer@example.com",
            password="trainerpass123", role=UserRole.TRAINER,
        )
        self.external: CustomUser = CustomUser.objects.create_user(
            username="external", email="external@example.com",
            password="externalpass123", role=UserRole.EXTERNAL,
        )
        self.category: Category = Category.objects.create(
            code="U14", description="Under 14", age_range="12-14",
        )
        self.trainer: Trainer = Trainer.objects.create(
            first_name="Carlo", last_name="Bianchi",
            fiscal_code="BNCCRL80A01H501Z", user=self.trainer_user,
        )
        self.athlete: Athlete = Athlete.objects.create(
            guardian=self.guardian,
            first_name="Luca", last_name="Rossi",
            fiscal_code="RSSLCU10A01H501Z",
            date_of_birth=datetime.date(2010, 1, 1),
            place_of_birth="Roma",
            category=self.category,
            trainer=self.trainer,
        )
        self.other_athlete: Athlete = Athlete.objects.create(
            guardian=self.other_guardian,
            first_name="Mario", last_name="Verdi",
            fiscal_code="VRDMRA10A01H501Z",
            date_of_birth=datetime.date(2010, 2, 1),
            place_of_birth="Milano",
            category=self.category,
        )
        self.doctor: SportDoctor = SportDoctor.objects.create(
            first_name="Giuseppe", last_name="Verdi",
            vat_number="12345678901",
        )
        self.certificate: SportCertificate = SportCertificate.objects.create(
            athlete=self.athlete,
            doctor=self.doctor,
            issue_date=datetime.date(2025, 9, 1),
            expiration_date=datetime.date(2026, 9, 1),
        )
        self.other_certificate: SportCertificate = SportCertificate.objects.create(
            athlete=self.other_athlete,
            doctor=self.doctor,
            issue_date=datetime.date(2025, 9, 5),
            expiration_date=datetime.date(2026, 9, 5),
        )


class CertificateListTests(CertificateSetupMixin, TestCase):
    """Tests for GET /api/v1/certificates/."""

    def test_admin_sees_all_certificates(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/certificates/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_member_sees_only_own_athletes(self) -> None:
        self.client.force_authenticate(user=self.guardian)
        response = self.client.get("/api/v1/certificates/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.certificate.pk)

    def test_trainer_sees_only_own_athletes(self) -> None:
        self.client.force_authenticate(user=self.trainer_user)
        response = self.client.get("/api/v1/certificates/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_unauthenticated_gets_401(self) -> None:
        response = self.client.get("/api/v1/certificates/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_external_cannot_list_certificates(self) -> None:
        self.client.force_authenticate(user=self.external)
        response = self.client.get("/api/v1/certificates/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CertificateCRUDTests(CertificateSetupMixin, TestCase):
    """Tests for certificate create/update/delete."""

    def test_admin_can_create_certificate(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/certificates/",
            {
                "athlete": self.other_athlete.pk,
                "doctor": self.doctor.pk,
                "issue_date": "2024-09-01",
                "expiration_date": "2025-09-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_operator_can_create_certificate(self) -> None:
        self.client.force_authenticate(user=self.operator)
        response = self.client.post(
            "/api/v1/certificates/",
            {
                "athlete": self.other_athlete.pk,
                "doctor": self.doctor.pk,
                "issue_date": "2024-09-01",
                "expiration_date": "2025-09-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_member_cannot_create_certificate(self) -> None:
        self.client.force_authenticate(user=self.guardian)
        response = self.client.post(
            "/api/v1/certificates/",
            {
                "athlete": self.athlete.pk,
                "doctor": self.doctor.pk,
                "issue_date": "2024-09-01",
                "expiration_date": "2025-09-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_external_cannot_create_certificate(self) -> None:
        self.client.force_authenticate(user=self.external)
        response = self.client.post(
            "/api/v1/certificates/",
            {
                "athlete": self.other_athlete.pk,
                "doctor": self.doctor.pk,
                "issue_date": "2024-09-01",
                "expiration_date": "2025-09-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_expiration_before_issue_returns_400(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/certificates/",
            {
                "athlete": self.athlete.pk,
                "doctor": self.doctor.pk,
                "issue_date": "2025-09-01",
                "expiration_date": "2025-08-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expiration_equal_to_issue_returns_400(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/certificates/",
            {
                "athlete": self.athlete.pk,
                "doctor": self.doctor.pk,
                "issue_date": "2025-09-01",
                "expiration_date": "2025-09-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_can_soft_delete_certificate(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/v1/certificates/{self.certificate.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.certificate.refresh_from_db()
        self.assertFalse(self.certificate.is_active)
