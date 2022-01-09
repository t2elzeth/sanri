import factory

from transport_companies.models import TransportCompany


class TransportCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TransportCompany

    name = factory.Faker("first_name")
