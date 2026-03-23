from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from athletes.models import Athlete, Category
from geography.models import Country
from staff.models import Trainer
from users.models import CustomUser, UserRole


class CategoryAPITests(TestCase):
    """Tests for /api/v1/categories/ endpoint."""

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
        self.category: Category = Category.objects.create(
            code="U14", description="Under 14", age_range="12-13",
        )

    def test_authenticated_can_list_categories(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.get("/api/v1/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_category(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/categories/",
            {"code": "U16", "description": "Under 16", "age_range": "14-15"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_member_cannot_create_category(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.post(
            "/api/v1/categories/",
            {"code": "U18", "description": "Under 18"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AthleteAPITests(TestCase):
    """Tests for /api/v1/athletes/ endpoint."""

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.admin: CustomUser = CustomUser.objects.create_user(
            username="admin", email="admin@example.com",
            password="adminpass123", role=UserRole.ADMIN,
        )
        self.member: CustomUser = CustomUser.objects.create_user(
            username="genitore", email="genitore@example.com",
            password="genpass123", role=UserRole.MEMBER,
        )
        self.other_member: CustomUser = CustomUser.objects.create_user(
            username="altro", email="altro@example.com",
            password="altropass123", role=UserRole.MEMBER,
        )
        self.category: Category = Category.objects.create(
            code="U14", description="Under 14",
        )
        self.athlete: Athlete = Athlete.objects.create(
            guardian=self.member,
            first_name="Davide",
            last_name="Rossi",
            fiscal_code="RSSDVD10A01H501A",
            date_of_birth="2010-01-01",
            place_of_birth="Roma",
            category=self.category,
        )

    def test_admin_can_list_all_athletes(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/athletes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_member_sees_only_own_athletes(self) -> None:
        self.client.force_authenticate(user=self.other_member)
        response = self.client.get("/api/v1/athletes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_guardian_sees_own_athletes(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.get("/api/v1/athletes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_admin_can_create_athlete(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/athletes/",
            {
                "guardian": self.member.pk,
                "first_name": "Marco",
                "last_name": "Bianchi",
                "fiscal_code": "BNCMRC12B01H501B",
                "date_of_birth": "2012-02-01",
                "place_of_birth": "Milano",
                "category": self.category.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_deactivate_athlete(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/v1/athletes/{self.athlete.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.athlete.refresh_from_db()
        self.assertFalse(self.athlete.is_active)

    def test_athlete_detail_exposes_nationality_fields(self) -> None:
        country: Country = Country.objects.create(name="Italia", iso_code="ITA")
        self.athlete.nationality = country
        self.athlete.save()
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"/api/v1/athletes/{self.athlete.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nationality"], country.pk)
        self.assertEqual(response.data["nationality_detail"]["iso_code"], "ITA")

    def test_athlete_detail_nationality_none_when_not_set(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"/api/v1/athletes/{self.athlete.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["nationality"])
        self.assertIsNone(response.data["nationality_detail"])

    def test_admin_can_set_nationality_on_create(self) -> None:
        country: Country = Country.objects.create(name="Francia", iso_code="FRA")
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/athletes/",
            {
                "guardian": self.member.pk,
                "first_name": "Luca",
                "last_name": "Verdi",
                "fiscal_code": "VRDLCU13C01H501C",
                "date_of_birth": "2013-03-01",
                "place_of_birth": "Torino",
                "category": self.category.pk,
                "nationality": country.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nationality"], country.pk)
