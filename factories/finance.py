import factory
from factory.django import DjangoModelFactory

from companies.models import Company
from invoices.models import Invoice, InvoiceDirection
from payment_methods.models import PaymentMethod
from receipts.models import Receipt
from factories.users import UserFactory


class CompanyFactory(DjangoModelFactory):
    """Factory for Company."""

    class Meta:
        model = Company

    business_name = factory.Faker("company", locale="it_IT")
    vat_number = factory.Sequence(lambda n: f"{n:011d}")
    fiscal_code = None
    vat_equals_fc = False
    is_active = True


class PaymentMethodFactory(DjangoModelFactory):
    """Factory for PaymentMethod."""

    class Meta:
        model = PaymentMethod
        django_get_or_create = ("name",)

    name = factory.Iterator(["Bonifico Bancario", "Contanti", "POS", "Assegno"])
    is_active = True


class InvoiceFactory(DjangoModelFactory):
    """Factory for Invoice."""

    class Meta:
        model = Invoice

    date = factory.Faker("date_between", start_date="-1y", end_date="today")
    number = factory.Sequence(lambda n: f"2025/{n:04d}")
    description = factory.Faker("sentence", nb_words=6, locale="it_IT")
    amount = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True, min_value=10, max_value=5000
    )
    direction = factory.Iterator([InvoiceDirection.PURCHASE, InvoiceDirection.SALE])
    company = factory.SubFactory(CompanyFactory)
    payment_method = factory.SubFactory(PaymentMethodFactory)
    is_active = True


class ReceiptFactory(DjangoModelFactory):
    """Factory for Receipt."""

    class Meta:
        model = Receipt

    date = factory.Faker("date_between", start_date="-1y", end_date="today")
    description = factory.Faker("sentence", nb_words=5, locale="it_IT")
    amount = factory.Faker(
        "pydecimal", left_digits=3, right_digits=2, positive=True, min_value=10, max_value=1000
    )
    user = factory.SubFactory(UserFactory)
    payment_method = factory.SubFactory(PaymentMethodFactory)
    is_active = True
