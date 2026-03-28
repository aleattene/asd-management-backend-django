import datetime

import factory
from factory.django import DjangoModelFactory

from certificates.models import SportCertificate
from factories.athletes import AthleteFactory
from factories.doctors import SportDoctorFactory


class SportCertificateFactory(DjangoModelFactory):
    """Factory for SportCertificate. issue_date is always before expiration_date."""

    class Meta:
        model = SportCertificate

    athlete = factory.SubFactory(AthleteFactory)
    doctor = factory.SubFactory(SportDoctorFactory)
    issue_date = factory.Faker("date_between", start_date="-1y", end_date="-1d")
    expiration_date = factory.LazyAttribute(
        lambda obj: obj.issue_date + datetime.timedelta(days=365)
    )
    is_active = True
