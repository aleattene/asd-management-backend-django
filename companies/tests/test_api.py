from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from companies.models import Company
from users.models import CustomUser, UserRole


class CompanyAPITests(TestCase):
    """Tests for /api/v1/companies/ endpoint."""

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
        self.company: Company = Company.objects.create(
            business_name="Palestra Sport S.r.l.",
            vat_number="12345678901",
            fiscal_code="12345678901",
            vat_equals_fc=True,
        )

    # --- LIST ---

    def test_admin_can_list_companies(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/companies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_operator_can_list_companies(self) -> None:
        self.client.force_authenticate(user=self.operator)
        response = self.client.get("/api/v1/companies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_cannot_list_companies(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.get("/api/v1/companies/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_list_companies(self) -> None:
        response = self.client.get("/api/v1/companies/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- CREATE ---

    def test_admin_can_create_company(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/companies/",
            {
                "business_name": "Nuova Palestra S.r.l.",
                "vat_number": "98765432101",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_operator_can_create_company(self) -> None:
        self.client.force_authenticate(user=self.operator)
        response = self.client.post(
            "/api/v1/companies/",
            {"business_name": "Operatore Palestra S.r.l."},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_member_cannot_create_company(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.post(
            "/api/v1/companies/",
            {"business_name": "Hacked S.r.l."},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- RETRIEVE ---

    def test_admin_can_retrieve_company(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"/api/v1/companies/{self.company.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["business_name"], "Palestra Sport S.r.l.")

    # --- UPDATE ---

    def test_admin_can_update_company(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            f"/api/v1/companies/{self.company.pk}/",
            {"business_name": "Palestra Sport Aggiornata S.r.l."},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.business_name, "Palestra Sport Aggiornata S.r.l.")

    # --- SOFT DELETE ---

    def test_admin_can_deactivate_company(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/v1/companies/{self.company.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.company.refresh_from_db()
        self.assertFalse(self.company.is_active)

    # --- NULLABLE FIELD NORMALIZATION ---

    def test_empty_vat_number_normalized_to_null(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/companies/",
            {"business_name": "Privato Senza P.IVA", "vat_number": ""},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["vat_number"])

    def test_empty_fiscal_code_normalized_to_null(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/companies/",
            {"business_name": "Ditta Estera Senza CF", "fiscal_code": ""},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["fiscal_code"])

    def test_deactivated_company_not_in_list(self) -> None:
        self.company.is_active = False
        self.company.save(update_fields=["is_active"])
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/companies/")
        self.assertEqual(response.data["count"], 0)
