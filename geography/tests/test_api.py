from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from geography.models import Country, Province, Municipality
from users.models import CustomUser, UserRole


class GeographySetupMixin:
    """Shared setup for geography API tests."""

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
        self.country: Country = Country.objects.create(
            name="Italia", iso_code="ITA"
        )
        self.province: Province = Province.objects.create(
            name="Roma", code="RM"
        )
        self.municipality: Municipality = Municipality.objects.create(
            name="Roma", province=self.province
        )


class CountryAPITests(GeographySetupMixin, TestCase):
    """Tests for /api/v1/countries/."""

    def test_admin_can_list_countries(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/countries/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_member_can_list_countries(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.get("/api/v1/countries/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_gets_401(self) -> None:
        response = self.client.get("/api/v1/countries/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_create_country(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/countries/",
            {"name": "Francia", "iso_code": "FRA"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_member_cannot_create_country(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.post(
            "/api/v1/countries/",
            {"name": "Francia", "iso_code": "FRA"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_operator_can_create_country(self) -> None:
        self.client.force_authenticate(user=self.operator)
        response = self.client.post(
            "/api/v1/countries/",
            {"name": "Germania", "iso_code": "DEU"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_trainer_can_list_countries(self) -> None:
        self.client.force_authenticate(user=self.trainer_user)
        response = self.client.get("/api/v1/countries/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trainer_cannot_create_country(self) -> None:
        self.client.force_authenticate(user=self.trainer_user)
        response = self.client.post(
            "/api/v1/countries/",
            {"name": "Germania", "iso_code": "DEU"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_external_cannot_list_countries(self) -> None:
        self.client.force_authenticate(user=self.external)
        response = self.client.get("/api/v1/countries/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProvinceAPITests(GeographySetupMixin, TestCase):
    """Tests for /api/v1/provinces/."""

    def test_admin_can_list_provinces(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/provinces/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_member_can_list_provinces(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.get("/api/v1/provinces/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_province(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/provinces/",
            {"name": "Milano", "code": "MI"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_member_cannot_create_province(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.post(
            "/api/v1/provinces/",
            {"name": "Milano", "code": "MI"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_trainer_can_list_provinces(self) -> None:
        self.client.force_authenticate(user=self.trainer_user)
        response = self.client.get("/api/v1/provinces/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_external_cannot_list_provinces(self) -> None:
        self.client.force_authenticate(user=self.external)
        response = self.client.get("/api/v1/provinces/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_list_provinces(self) -> None:
        response = self.client.get("/api/v1/provinces/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MunicipalityAPITests(GeographySetupMixin, TestCase):
    """Tests for /api/v1/municipalities/."""

    def test_admin_can_list_municipalities(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/municipalities/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_member_can_list_municipalities(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.get("/api/v1/municipalities/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_province(self) -> None:
        other_province: Province = Province.objects.create(
            name="Milano", code="MI"
        )
        Municipality.objects.create(name="Milano", province=other_province)
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(
            f"/api/v1/municipalities/?province={self.province.pk}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Roma")

    def test_admin_can_create_municipality(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/municipalities/",
            {"name": "Ostia", "province": self.province.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_member_cannot_create_municipality(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.post(
            "/api/v1/municipalities/",
            {"name": "Ostia", "province": self.province.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_trainer_can_list_municipalities(self) -> None:
        self.client.force_authenticate(user=self.trainer_user)
        response = self.client.get("/api/v1/municipalities/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_external_cannot_list_municipalities(self) -> None:
        self.client.force_authenticate(user=self.external)
        response = self.client.get("/api/v1/municipalities/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_list_municipalities(self) -> None:
        response = self.client.get("/api/v1/municipalities/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
