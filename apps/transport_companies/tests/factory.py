from transport_companies.models import TransportCompany

import factory


class TransportCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TransportCompany

    name = factory.Faker("first_name")
