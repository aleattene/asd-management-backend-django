from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from payment_methods.models import PaymentMethod
from users.models import CustomUser, UserRole


class PaymentMethodAPITests(TestCase):
    """Tests for /api/v1/payment-methods/ endpoint."""

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
        self.payment_method: PaymentMethod = PaymentMethod.objects.create(
            name="Contanti",
        )

    # --- LIST ---

    def test_admin_can_list_payment_methods(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/payment-methods/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_operator_can_list_payment_methods(self) -> None:
        self.client.force_authenticate(user=self.operator)
        response = self.client.get("/api/v1/payment-methods/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_cannot_list_payment_methods(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.get("/api/v1/payment-methods/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_list_payment_methods(self) -> None:
        response = self.client.get("/api/v1/payment-methods/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- CREATE ---

    def test_admin_can_create_payment_method(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/payment-methods/",
            {"name": "Bonifico"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_operator_can_create_payment_method(self) -> None:
        self.client.force_authenticate(user=self.operator)
        response = self.client.post(
            "/api/v1/payment-methods/",
            {"name": "Bancomat"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_member_cannot_create_payment_method(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.post(
            "/api/v1/payment-methods/",
            {"name": "Bonifico"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- UPDATE ---

    def test_admin_can_update_payment_method(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            f"/api/v1/payment-methods/{self.payment_method.pk}/",
            {"name": "Contanti (cash)"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment_method.refresh_from_db()
        self.assertEqual(self.payment_method.name, "Contanti (cash)")

    # --- SOFT DELETE ---

    def test_admin_can_deactivate_payment_method(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/v1/payment-methods/{self.payment_method.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.payment_method.refresh_from_db()
        self.assertFalse(self.payment_method.is_active)

    def test_deactivated_payment_method_not_in_list(self) -> None:
        self.payment_method.is_active = False
        self.payment_method.save(update_fields=["is_active"])
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/payment-methods/")
        self.assertEqual(response.data["count"], 0)
