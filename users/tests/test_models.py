from django.db import IntegrityError
from django.test import TestCase

from users.models import CustomUser, UserRole


class CustomUserManagerTests(TestCase):
    """Tests for CustomUserManager."""

    def test_create_user(self) -> None:
        user: CustomUser = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.role, UserRole.MEMBER)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password("testpass123"))

    def test_create_user_without_email_raises(self) -> None:
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                username="testuser", email="", password="testpass123"
            )

    def test_create_superuser(self) -> None:
        admin: CustomUser = CustomUser.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, UserRole.SUPERADMIN)

    def test_create_superuser_not_staff_raises(self) -> None:
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="adminpass123",
                is_staff=False,
            )

    def test_create_superuser_not_superuser_raises(self) -> None:
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="adminpass123",
                is_superuser=False,
            )


class CustomUserModelTests(TestCase):
    """Tests for CustomUser model."""

    def setUp(self) -> None:
        self.user: CustomUser = CustomUser.objects.create_user(
            username="mario",
            email="mario@example.com",
            password="testpass123",
            first_name="Mario",
            last_name="Rossi",
            fiscal_code="RSSMRA80A01H501Z",
            role=UserRole.MEMBER,
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.user), "mario (mario@example.com)")

    def test_repr(self) -> None:
        self.assertEqual(repr(self.user), "CustomUser(username=mario, role=member)")

    def test_email_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                username="altro",
                email="mario@example.com",
                password="testpass123",
            )

    def test_fiscal_code_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                username="altro",
                email="altro@example.com",
                password="testpass123",
                fiscal_code="RSSMRA80A01H501Z",
            )

    def test_default_role_is_member(self) -> None:
        user: CustomUser = CustomUser.objects.create_user(
            username="default", email="default@example.com", password="testpass123"
        )
        self.assertEqual(user.role, UserRole.MEMBER)

    def test_is_authorized_default_false(self) -> None:
        self.assertFalse(self.user.is_authorized)

    def test_address_fields_default_empty(self) -> None:
        self.assertEqual(self.user.address_street, "")
        self.assertEqual(self.user.address_number, "")
        self.assertEqual(self.user.address_zip, "")
        self.assertIsNone(self.user.municipality)
