from rest_framework.test import APITestCase

from auction.models import Auction
from authorization.models import User
from car_model.models import CarMark

from rest_framework.reverse import reverse


class TestCreateNewCarSale(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("car-sale-list-create")
        self.ownerClient = User.objects.create_user(
            password="123",
            fullName="My owner client",
            country="KG",
            email="ownerclient@gmail.com",
            phoneNumber="+996771221103",
            service=User.SERVICE_ENTIRE,
            atWhatPrice=User.AT_WHAT_PRICE_BY_FACT,
            username="owner_client",
        )

        self.auction = Auction.objects.create(
            name="AuctionName",
            parkingPrice1=25000,
            parkingPrice2=20000,
            parkingPrice3=15000,
            parkingPrice4=10000,
        )

        self.car_mark = CarMark.objects.create(name="HONDA")
        self.car_model = self.car_mark.models.create(name="FIT")

    def test_create(self):
        payload = {
            "ownerClient_id": self.ownerClient.id,
            "auction_id": self.auction.id,
            "carOrder_id": self.car_model.id,
            "vinNumber": "255",
            "auctionFees": 25000,
            "salesFees": 25000,
            "status": False,
        }
        response = self.client.post(self.url)
