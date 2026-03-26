import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from athletes.models import Athlete, Category
from enrollments.models import Enrollment
from staff.models import Trainer
from users.models import CustomUser, UserRole


class EnrollmentSetupMixin:
    """Shared setup for enrollment API tests."""

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
        self.enrollment: Enrollment = Enrollment.objects.create(
            athlete=self.athlete,
            season="2025/2026",
            enrollment_date=datetime.date(2025, 9, 1),
        )
        self.other_enrollment: Enrollment = Enrollment.objects.create(
            athlete=self.other_athlete,
            season="2025/2026",
            enrollment_date=datetime.date(2025, 9, 5),
        )


class EnrollmentListTests(EnrollmentSetupMixin, TestCase):
    """Tests for GET /api/v1/enrollments/."""

    def test_admin_sees_all_enrollments(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/enrollments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_member_sees_only_own_athletes(self) -> None:
        self.client.force_authenticate(user=self.guardian)
        response = self.client.get("/api/v1/enrollments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.enrollment.pk)

    def test_trainer_sees_only_own_athletes(self) -> None:
        self.client.force_authenticate(user=self.trainer_user)
        response = self.client.get("/api/v1/enrollments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_unauthenticated_gets_401(self) -> None:
        response = self.client.get("/api/v1/enrollments/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_external_cannot_list_enrollments(self) -> None:
        self.client.force_authenticate(user=self.external)
        response = self.client.get("/api/v1/enrollments/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EnrollmentCRUDTests(EnrollmentSetupMixin, TestCase):
    """Tests for enrollment create/update/delete."""

    def test_admin_can_create_enrollment(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/enrollments/",
            {
                "athlete": self.athlete.pk,
                "season": "2024/2025",
                "enrollment_date": "2024-09-01",
                "guardian_signed": True,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_operator_can_create_enrollment(self) -> None:
        self.client.force_authenticate(user=self.operator)
        response = self.client.post(
            "/api/v1/enrollments/",
            {
                "athlete": self.athlete.pk,
                "season": "2024/2025",
                "enrollment_date": "2024-09-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_member_cannot_create_enrollment(self) -> None:
        self.client.force_authenticate(user=self.guardian)
        response = self.client.post(
            "/api/v1/enrollments/",
            {
                "athlete": self.athlete.pk,
                "season": "2024/2025",
                "enrollment_date": "2024-09-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_external_cannot_create_enrollment(self) -> None:
        self.client.force_authenticate(user=self.external)
        response = self.client.post(
            "/api/v1/enrollments/",
            {
                "athlete": self.athlete.pk,
                "season": "2023/2024",
                "enrollment_date": "2023-09-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_season_format_returns_400(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/enrollments/",
            {
                "athlete": self.athlete.pk,
                "season": "25/26",
                "enrollment_date": "2025-09-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_enrollment_per_season_returns_400(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/enrollments/",
            {
                "athlete": self.athlete.pk,
                "season": "2025/2026",
                "enrollment_date": "2025-09-10",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_can_soft_delete_enrollment(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/v1/enrollments/{self.enrollment.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.enrollment.refresh_from_db()
        self.assertFalse(self.enrollment.is_active)
