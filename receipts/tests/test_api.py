from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from payment_methods.models import PaymentMethod
from receipts.models import Receipt
from users.models import CustomUser, UserRole


class ReceiptAPITests(TestCase):
    """Tests for /api/v1/receipts/ endpoint."""

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.admin: CustomUser = CustomUser.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            role=UserRole.ADMIN,
        )
        self.operator: CustomUser = CustomUser.objects.create_user(
            username="operator",
            email="operator@example.com",
            password="operatorpass123",
            role=UserRole.OPERATOR,
        )
        self.member: CustomUser = CustomUser.objects.create_user(
            username="member",
            email="member@example.com",
            password="memberpass123",
            role=UserRole.MEMBER,
        )
        self.trainer: CustomUser = CustomUser.objects.create_user(
            username="trainer",
            email="trainer@example.com",
            password="trainerpass123",
            role=UserRole.TRAINER,
        )
        self.external: CustomUser = CustomUser.objects.create_user(
            username="external",
            email="external@example.com",
            password="externalpass123",
            role=UserRole.EXTERNAL,
        )
        self.payment_method: PaymentMethod = PaymentMethod.objects.create(
            name="Contanti",
        )
        self.receipt: Receipt = Receipt.objects.create(
            date="2026-01-15",
            description="Quota iscrizione stagione 2025/2026",
            amount="150.00",
            user=self.member,
            payment_method=self.payment_method,
        )

    # --- LIST ---

    def test_admin_can_list_receipts(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/receipts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_operator_can_list_receipts(self) -> None:
        self.client.force_authenticate(user=self.operator)
        response = self.client.get("/api/v1/receipts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_cannot_list_receipts(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.get("/api/v1/receipts/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_list_receipts(self) -> None:
        response = self.client.get("/api/v1/receipts/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_trainer_cannot_list_receipts(self) -> None:
        self.client.force_authenticate(user=self.trainer)
        response = self.client.get("/api/v1/receipts/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_external_cannot_list_receipts(self) -> None:
        self.client.force_authenticate(user=self.external)
        response = self.client.get("/api/v1/receipts/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- CREATE ---

    def test_admin_can_create_receipt(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/receipts/",
            {
                "date": "2026-02-01",
                "description": "Materiale sportivo",
                "amount": "50.00",
                "user": self.member.pk,
                "payment_method": self.payment_method.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_operator_can_create_receipt(self) -> None:
        self.client.force_authenticate(user=self.operator)
        response = self.client.post(
            "/api/v1/receipts/",
            {
                "date": "2026-02-15",
                "description": "Quota mensile",
                "amount": "30.00",
                "user": self.member.pk,
                "payment_method": self.payment_method.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_member_cannot_create_receipt(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.post(
            "/api/v1/receipts/",
            {
                "date": "2026-02-01",
                "description": "Non autorizzato",
                "amount": "100.00",
                "user": self.member.pk,
                "payment_method": self.payment_method.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- RETRIEVE ---

    def test_admin_can_retrieve_receipt(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"/api/v1/receipts/{self.receipt.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "Quota iscrizione stagione 2025/2026")

    # --- UPDATE ---

    def test_admin_can_update_receipt(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            f"/api/v1/receipts/{self.receipt.pk}/",
            {"description": "Quota aggiornata"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.receipt.refresh_from_db()
        self.assertEqual(self.receipt.description, "Quota aggiornata")

    # --- SOFT DELETE ---

    def test_admin_can_deactivate_receipt(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/v1/receipts/{self.receipt.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.receipt.refresh_from_db()
        self.assertFalse(self.receipt.is_active)

    def test_deactivated_receipt_not_in_list(self) -> None:
        self.receipt.is_active = False
        self.receipt.save(update_fields=["is_active"])
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/receipts/")
        self.assertEqual(response.data["count"], 0)
