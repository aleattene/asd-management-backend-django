import factory
from factory.django import DjangoModelFactory

from doctors.models import SportDoctor


class SportDoctorFactory(DjangoModelFactory):
    """Factory for SportDoctor."""

    class Meta:
        model = SportDoctor

    first_name = factory.Faker("first_name", locale="it_IT")
    last_name = factory.Faker("last_name", locale="it_IT")
    vat_number = factory.Sequence(lambda n: f"{n:011d}")
    is_active = True
