from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import CustomUser, UserRole


class JWTAuthTests(TestCase):
    """Tests for JWT authentication endpoints."""

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.user: CustomUser = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )

    def test_obtain_token(self) -> None:
        response = self.client.post(
            "/api/v1/auth/token/",
            {"username": "testuser", "password": "testpass123"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_obtain_token_wrong_password(self) -> None:
        response = self.client.post(
            "/api/v1/auth/token/",
            {"username": "testuser", "password": "wrong"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self) -> None:
        token_response = self.client.post(
            "/api/v1/auth/token/",
            {"username": "testuser", "password": "testpass123"},
        )
        refresh: str = token_response.data["refresh"]
        response = self.client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": refresh},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)


class UserMeTests(TestCase):
    """Tests for /api/v1/users/me/ endpoint."""

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.user: CustomUser = CustomUser.objects.create_user(
            username="mario",
            email="mario@example.com",
            password="testpass123",
            first_name="Mario",
            last_name="Rossi",
            role=UserRole.MEMBER,
        )
        self.client.force_authenticate(user=self.user)

    def test_get_me(self) -> None:
        response = self.client.get("/api/v1/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "mario")
        self.assertEqual(response.data["email"], "mario@example.com")
        self.assertEqual(response.data["role"], "member")

    def test_patch_me(self) -> None:
        response = self.client.patch(
            "/api/v1/users/me/",
            {"phone_number": "3331234567"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], "3331234567")

    def test_me_cannot_change_role(self) -> None:
        response = self.client.patch(
            "/api/v1/users/me/",
            {"role": "admin"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], "member")

    def test_me_unauthenticated(self) -> None:
        client = APIClient()
        response = client.get("/api/v1/users/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserCRUDTests(TestCase):
    """Tests for user CRUD (admin/operator only)."""

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

    def test_admin_can_list_users(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_operator_can_list_users(self) -> None:
        self.client.force_authenticate(user=self.operator)
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_cannot_list_users(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_user(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/v1/users/",
            {
                "username": "newuser",
                "email": "new@example.com",
                "password": "newpass123",
                "first_name": "Nuovo",
                "last_name": "Utente",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username="newuser").exists())

    def test_member_cannot_create_user(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.post(
            "/api/v1/users/",
            {
                "username": "hacker",
                "email": "hack@example.com",
                "password": "hackpass123",
                "role": "admin",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_deactivate_user(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/v1/users/{self.member.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.member.refresh_from_db()
        self.assertFalse(self.member.is_active)

    def test_admin_can_retrieve_user(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"/api/v1/users/{self.member.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "member")
