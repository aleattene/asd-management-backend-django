from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from staff.models import Trainer, SportDoctor
from users.models import CustomUser, UserRole


class TrainerAPITests(TestCase):
    """Tests for /api/v1/trainers/ endpoint."""

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
        self.trainer: Trainer = Trainer.objects.create(
            first_name="Luca",
            last_name="Bianchi",
            fiscal_code="BNCLCU85B15H501X",
        )

    def test_admin_can_list_trainers(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/trainers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_cannot_list_trainers(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.get("/api/v1/trainers/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_trainer(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/trainers/",
            {
                "first_name": "Marco",
                "last_name": "Verdi",
                "fiscal_code": "VRDMRC90C01H501Y",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_deactivate_trainer(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/v1/trainers/{self.trainer.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.trainer.refresh_from_db()
        self.assertFalse(self.trainer.is_active)


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
