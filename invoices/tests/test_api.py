from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from companies.models import Company
from invoices.models import Invoice, InvoiceDirection
from payment_methods.models import PaymentMethod
from users.models import CustomUser, UserRole


class InvoiceAPITests(TestCase):
    """Tests for /api/v1/invoices/ endpoint."""

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
        self.company: Company = Company.objects.create(
            business_name="Fornitore S.r.l.",
            vat_number="12345678901",
        )
        self.payment_method: PaymentMethod = PaymentMethod.objects.create(
            name="Bonifico",
        )
        self.invoice: Invoice = Invoice.objects.create(
            date="2026-01-15",
            number="2026/001",
            description="Materiale sportivo",
            amount="1500.00",
            direction=InvoiceDirection.PURCHASE,
            company=self.company,
            payment_method=self.payment_method,
        )

    # --- LIST ---

    def test_admin_can_list_invoices(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/invoices/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_operator_can_list_invoices(self) -> None:
        self.client.force_authenticate(user=self.operator)
        response = self.client.get("/api/v1/invoices/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_cannot_list_invoices(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.get("/api/v1/invoices/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_list_invoices(self) -> None:
        response = self.client.get("/api/v1/invoices/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_trainer_cannot_list_invoices(self) -> None:
        self.client.force_authenticate(user=self.trainer)
        response = self.client.get("/api/v1/invoices/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_external_cannot_list_invoices(self) -> None:
        self.client.force_authenticate(user=self.external)
        response = self.client.get("/api/v1/invoices/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- CREATE ---

    def test_admin_can_create_invoice(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/invoices/",
            {
                "date": "2026-02-01",
                "number": "2026/002",
                "description": "Nuovo acquisto",
                "amount": "750.00",
                "direction": "purchase",
                "company": self.company.pk,
                "payment_method": self.payment_method.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_operator_can_create_invoice(self) -> None:
        self.client.force_authenticate(user=self.operator)
        response = self.client.post(
            "/api/v1/invoices/",
            {
                "date": "2026-02-15",
                "number": "2026/003",
                "description": "Acquisto operatore",
                "amount": "300.00",
                "direction": "purchase",
                "company": self.company.pk,
                "payment_method": self.payment_method.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_member_cannot_create_invoice(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.post(
            "/api/v1/invoices/",
            {
                "date": "2026-02-01",
                "number": "2026/999",
                "description": "Non autorizzato",
                "amount": "100.00",
                "direction": "purchase",
                "company": self.company.pk,
                "payment_method": self.payment_method.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- RETRIEVE ---

    def test_admin_can_retrieve_invoice(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"/api/v1/invoices/{self.invoice.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number"], "2026/001")

    # --- UPDATE ---

    def test_admin_can_update_invoice(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            f"/api/v1/invoices/{self.invoice.pk}/",
            {"description": "Materiale sportivo aggiornato"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.description, "Materiale sportivo aggiornato")

    # --- SOFT DELETE ---

    def test_admin_can_deactivate_invoice(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/v1/invoices/{self.invoice.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.invoice.refresh_from_db()
        self.assertFalse(self.invoice.is_active)

    def test_deactivated_invoice_not_in_list(self) -> None:
        self.invoice.is_active = False
        self.invoice.save(update_fields=["is_active"])
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/invoices/")
        self.assertEqual(response.data["count"], 0)

    # --- DIRECTION VALIDATION ---

    def test_invalid_direction_rejected(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/invoices/",
            {
                "date": "2026-03-01",
                "number": "2026/ERR",
                "description": "Direzione invalida",
                "amount": "100.00",
                "direction": "invalid",
                "company": self.company.pk,
                "payment_method": self.payment_method.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
