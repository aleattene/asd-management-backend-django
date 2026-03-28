import factory
from factory.django import DjangoModelFactory

from enrollments.models import Enrollment
from factories.athletes import AthleteFactory


class EnrollmentFactory(DjangoModelFactory):
    """Factory for Enrollment."""

    class Meta:
        model = Enrollment

    athlete = factory.SubFactory(AthleteFactory)
    season = "2025/2026"
    enrollment_date = factory.Faker("date_between", start_date="-6m", end_date="today")
    guardian_signed = factory.Faker("boolean", chance_of_getting_true=80)
    is_active = True
