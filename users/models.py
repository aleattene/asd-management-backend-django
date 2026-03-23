from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserRole(models.TextChoices):
    """Roles available in the platform."""

    SUPERADMIN = "superadmin", "Super Admin Tecnico"
    ADMIN = "admin", "Amministratore"
    OPERATOR = "operator", "Operatore Amministrativo"
    TRAINER = "trainer", "Allenatore"
    MEMBER = "member", "Membro"


class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser."""

    def create_user(
        self,
        username: str,
        email: str,
        password: str | None = None,
        **extra_fields,
    ) -> "CustomUser":
        """Create and save a regular user."""
        if not email:
            raise ValueError("The email field is required.")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user: CustomUser = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username: str,
        email: str,
        password: str | None = None,
        **extra_fields,
    ) -> "CustomUser":
        """Create and save a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UserRole.SUPERADMIN)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model with role-based access."""

    email = models.EmailField(unique=True)
    fiscal_code = models.CharField(
        max_length=16, unique=True, blank=True, null=True, verbose_name="Codice Fiscale"
    )
    phone_number = models.CharField(
        max_length=20, blank=True, default="", verbose_name="Telefono"
    )
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name="Data di Nascita"
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.MEMBER,
        verbose_name="Ruolo",
    )
    address_street = models.CharField(
        max_length=200, blank=True, default="", verbose_name="Via"
    )
    address_number = models.CharField(
        max_length=10, blank=True, default="", verbose_name="Civico"
    )
    address_zip = models.CharField(
        max_length=5, blank=True, default="", verbose_name="CAP"
    )
    municipality = models.ForeignKey(
        "geography.Municipality",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Comune",
    )
    is_authorized = models.BooleanField(
        default=False, verbose_name="Autorizzato"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    REQUIRED_FIELDS: list[str] = ["email"]

    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"

    def __repr__(self) -> str:
        return f"CustomUser(username={self.username}, role={self.role})"
