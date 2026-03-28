import factory
from factory.django import DjangoModelFactory

from staff.models import Trainer
from users.models import UserRole
from factories.users import UserFactory


class TrainerFactory(DjangoModelFactory):
    """Factory for Trainer."""

    class Meta:
        model = Trainer

    user = factory.SubFactory(UserFactory, role=UserRole.TRAINER)
    first_name = factory.LazyAttribute(lambda obj: obj.user.first_name)
    last_name = factory.LazyAttribute(lambda obj: obj.user.last_name)
    fiscal_code = factory.Sequence(lambda n: f"TRNFCT{n:02d}A01H501Z"[:16])
    is_active = True
