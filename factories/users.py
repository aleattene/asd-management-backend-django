import factory
from factory.django import DjangoModelFactory

from users.models import CustomUser, UserRole


class UserFactory(DjangoModelFactory):
    """Factory for CustomUser. Generates a member by default."""

    class Meta:
        model = CustomUser
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n:03d}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name", locale="it_IT")
    last_name = factory.Faker("last_name", locale="it_IT")
    password = factory.PostGenerationMethodCall("set_password", "Testpass123!")
    role = UserRole.MEMBER
    is_active = True
    is_authorized = True
    fiscal_code = factory.Sequence(lambda n: f"RSSMRA{n:02d}A01H501Z"[:16])
    phone_number = factory.Faker("phone_number", locale="it_IT")
    date_of_birth = factory.Faker("date_of_birth", minimum_age=18, maximum_age=60)
