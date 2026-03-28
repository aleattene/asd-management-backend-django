import factory
from factory.django import DjangoModelFactory

from athletes.models import Athlete, Category
from factories.users import UserFactory


class CategoryFactory(DjangoModelFactory):
    """Factory for Category."""

    class Meta:
        model = Category
        django_get_or_create = ("code",)

    code = factory.Sequence(lambda n: f"CAT{n:02d}")
    description = factory.Faker("bs", locale="it_IT")
    age_range = factory.Iterator(["6-8", "9-11", "12-14", "15-17", "18+"])
    is_active = True


class AthleteFactory(DjangoModelFactory):
    """Factory for Athlete."""

    class Meta:
        model = Athlete

    guardian = factory.SubFactory(UserFactory)
    first_name = factory.Faker("first_name", locale="it_IT")
    last_name = factory.Faker("last_name", locale="it_IT")
    fiscal_code = factory.Sequence(lambda n: f"ATLFCT{n:02d}A01H501Z"[:16])
    date_of_birth = factory.Faker("date_of_birth", minimum_age=6, maximum_age=18)
    place_of_birth = factory.Faker("city", locale="it_IT")
    category = factory.SubFactory(CategoryFactory)
    is_active = True
