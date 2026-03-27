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

    def test_refresh_token_rotation_returns_new_refresh(self) -> None:
        """Refresh should return a new refresh token (ROTATE_REFRESH_TOKENS=True)."""
        token_response = self.client.post(
            "/api/v1/auth/token/",
            {"username": "testuser", "password": "testpass123"},
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", token_response.data)
        old_refresh: str = token_response.data["refresh"]
        response = self.client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": old_refresh},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertNotEqual(response.data["refresh"], old_refresh)

    def test_refresh_token_blacklisted_after_rotation(self) -> None:
        """Old refresh token must be rejected after rotation (BLACKLIST_AFTER_ROTATION=True)."""
        token_response = self.client.post(
            "/api/v1/auth/token/",
            {"username": "testuser", "password": "testpass123"},
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", token_response.data)
        old_refresh: str = token_response.data["refresh"]
        # Use the refresh token once — it gets rotated and blacklisted
        first_refresh = self.client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": old_refresh},
        )
        self.assertEqual(first_refresh.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", first_refresh.data)
        self.assertNotEqual(first_refresh.data["refresh"], old_refresh)
        # Attempt to reuse the old refresh token — should fail
        response = self.client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": old_refresh},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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

    def test_external_cannot_access_me(self) -> None:
        external: CustomUser = CustomUser.objects.create_user(
            username="external_me",
            email="external_me@example.com",
            password="externalpass123",
            role=UserRole.EXTERNAL,
        )
        self.client.force_authenticate(user=external)
        response = self.client.get("/api/v1/users/me/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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
        self.external: CustomUser = CustomUser.objects.create_user(
            username="external",
            email="external@example.com",
            password="externalpass123",
            role=UserRole.EXTERNAL,
        )
        self.trainer: CustomUser = CustomUser.objects.create_user(
            username="trainer",
            email="trainer@example.com",
            password="trainerpass123",
            role=UserRole.TRAINER,
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

    def test_external_cannot_list_users(self) -> None:
        self.client.force_authenticate(user=self.external)
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_trainer_cannot_list_users(self) -> None:
        self.client.force_authenticate(user=self.trainer)
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_list_users(self) -> None:
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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


class UserRoleChangeTests(TestCase):
    """Tests for PATCH /api/v1/users/{id}/set_role/ endpoint."""

    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.superadmin: CustomUser = CustomUser.objects.create_user(
            username="superadmin",
            email="superadmin@example.com",
            password="superpass123",
            role=UserRole.SUPERADMIN,
        )
        self.admin: CustomUser = CustomUser.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            role=UserRole.ADMIN,
        )
        self.member: CustomUser = CustomUser.objects.create_user(
            username="member",
            email="member@example.com",
            password="memberpass123",
            role=UserRole.MEMBER,
        )

    def test_superadmin_can_change_role(self) -> None:
        self.client.force_authenticate(user=self.superadmin)
        response = self.client.patch(
            f"/api/v1/users/{self.member.pk}/set_role/",
            {"role": "trainer"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], "trainer")
        self.member.refresh_from_db()
        self.assertEqual(self.member.role, "trainer")

    def test_superadmin_can_assign_external_role(self) -> None:
        self.client.force_authenticate(user=self.superadmin)
        response = self.client.patch(
            f"/api/v1/users/{self.member.pk}/set_role/",
            {"role": "external"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], "external")
        self.member.refresh_from_db()
        self.assertEqual(self.member.role, "external")

    def test_admin_cannot_change_role(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            f"/api/v1/users/{self.member.pk}/set_role/",
            {"role": "operator"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_member_cannot_change_role(self) -> None:
        self.client.force_authenticate(user=self.member)
        response = self.client.patch(
            f"/api/v1/users/{self.member.pk}/set_role/",
            {"role": "admin"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_change_role(self) -> None:
        response = self.client.patch(
            f"/api/v1/users/{self.member.pk}/set_role/",
            {"role": "admin"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_role_returns_400(self) -> None:
        self.client.force_authenticate(user=self.superadmin)
        response = self.client.patch(
            f"/api/v1/users/{self.member.pk}/set_role/",
            {"role": "god"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_role_returns_400(self) -> None:
        self.client.force_authenticate(user=self.superadmin)
        response = self.client.patch(
            f"/api/v1/users/{self.member.pk}/set_role/",
            {},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
