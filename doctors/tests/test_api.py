from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from doctors.models import SportDoctor
from users.models import CustomUser, UserRole


class SportDoctorAPITests(TestCase):
    """Tests for /api/v1/doctors/ endpoint."""

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.admin: CustomUser = CustomUser.objects.create_user(
            username="admin", email="admin@example.com",
            password="adminpass123", role=UserRole.ADMIN,
        )
        self.member: CustomUser = CustomUser.objects.create_user(
            username="member", email="member@example.com",
            password="memberpass123", role=UserRole.MEMBER,
        )
        self.operator: CustomUser = CustomUser.objects.create_user(
            username="operator", email="operator@example.com",
            password="operatorpass123", role=UserRole.OPERATOR,
        )
        self.trainer_user: CustomUser = CustomUser.objects.create_user(
            username="trainer_user", email="trainer_user@example.com",
            password="trainerpass123", role=UserRole.TRAINER,
        )
        self.external: CustomUser = CustomUser.objects.create_user(
            username="external", email="external@example.com",
            password="externalpass123", role=UserRole.EXTERNAL,
        )
        self.doctor: SportDoctor = SportDoctor.objects.create(
            first_name="Giuseppe",
            last_name="Verdi",
            vat_number="12345678901",
        )

    def test_admin_can_list_doctors(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/doctors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_cannot_list_doctors(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.get("/api/v1/doctors/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_list_doctors(self) -> None:
        response = self.client.get("/api/v1/doctors/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_create_doctor(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/doctors/",
            {
                "first_name": "Anna",
                "last_name": "Rossi",
                "vat_number": "98765432101",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_deactivate_doctor(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/v1/doctors/{self.doctor.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.doctor.refresh_from_db()
        self.assertFalse(self.doctor.is_active)

    def test_operator_can_list_doctors(self) -> None:
        self.client.force_authenticate(user=self.operator)
        response = self.client.get("/api/v1/doctors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trainer_cannot_list_doctors(self) -> None:
        self.client.force_authenticate(user=self.trainer_user)
        response = self.client.get("/api/v1/doctors/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_external_cannot_list_doctors(self) -> None:
        self.client.force_authenticate(user=self.external)
        response = self.client.get("/api/v1/doctors/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
