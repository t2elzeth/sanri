import factory

from auction.tests.factory import AuctionFactory
from authorization.tests.factory import ClientFactory
from car_model.tests.factory import CarModelFactory
from car_order.models import CarOrder
from transport_companies.tests.factory import TransportCompanyFactory


class CarOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarOrder

    client = factory.SubFactory(ClientFactory)
    auction = factory.SubFactory(AuctionFactory)
    lotNumber = factory.Faker("pyint", min_value=1, max_value=10)
    carModel = factory.SubFactory(CarModelFactory)
    vinNumber = factory.Faker("bothify", text="CarVin: ????-###?#?#")
    year = factory.Faker("year")
    price = factory.Faker("pyint", min_value=1, max_value=100_000_000)
    recycle = factory.Faker("pyint", min_value=1, max_value=100_000)
    auctionFees = factory.Faker("pyint", min_value=1, max_value=1_000_000)
    transport = factory.Faker("pyint", min_value=1, max_value=10_000)
    amount = factory.Faker("pyint", min_value=1, max_value=100)
    transportCompany = factory.SubFactory(TransportCompanyFactory)

    carNumber = factory.Iterator(CarOrder.CAR_NUMBER_STATUS_CHOICES)
    documentsGiven = False
