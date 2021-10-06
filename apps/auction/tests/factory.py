from auction.models import Auction

import factory


class AuctionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Auction

    name = factory.Faker("first_name")
    parkingPrice1 = factory.Faker("numerify", text="%%%%")
    parkingPrice2 = factory.Faker("numerify", text="%%%%")
    parkingPrice3 = factory.Faker("numerify", text="%%%%")
    parkingPrice4 = factory.Faker("numerify", text="%%%%")
