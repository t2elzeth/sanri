import factory

from car_model.models import CarMark, CarModel


class CarMarkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarMark

    name = factory.Faker("first_name")


class CarModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarModel

    mark = factory.SubFactory(CarMarkFactory)
    name = factory.Faker("first_name")
