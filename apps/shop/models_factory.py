import factory
from authorization.tests.factory import ClientFactory
from car_model.tests.factory import CarModelFactory

from . import models


class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Car

    model = factory.SubFactory(CarModelFactory)
    year = factory.Faker("pyint", min_value=0, max_value=1000)
    volume = factory.Faker("pydecimal", left_digits=2, right_digits=2)
    mileage = factory.Faker("pydecimal", left_digits=15, right_digits=2)
    condition = factory.Faker("pyint", min_value=0, max_value=1000)
    price = factory.Faker("pydecimal", left_digits=15, right_digits=2)
    description = factory.Faker("paragraph", nb_sentences=3)


class BuyRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BuyRequest

    from_client = factory.SubFactory(ClientFactory)
    car = factory.SubFactory(CarFactory)
