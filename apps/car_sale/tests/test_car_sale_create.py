from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from auction.models import Auction
from authorization.models import User
from car_model.models import CarMark
from car_order.models import CarOrder
from car_sale.models import CarSale


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

        self.carOrder = CarOrder.objects.create(
            client=self.ownerClient,
            auction=self.auction,
            lotNumber=25000,
            carModel=self.car_model,
            vinNumber=25000,
            year=2019,
            fob=self.ownerClient.sizeFOB,
            price=50000,
            recycle=20000,
            auctionFees=25000,
            transport=3000,
            carNumber=CarOrder.CAR_NUMBER_NOT_GIVEN,
        )

        self.carSale = CarSale.objects.create(
            ownerClient=self.ownerClient,
            auction=self.auction,
            carOrder=self.carOrder,
            auctionFees=25000,
            salesFees=25000,
        )

    def test_create(self):
        payload = {
            "ownerClient_id": self.ownerClient.id,
            "auction_id": self.auction.id,
            "carOrder_id": self.carOrder.id,
            "auctionFees": 25000,
            "salesFees": 25000,
            "status": False,
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_status_set_to_true(self):
        self.url = reverse("car-sale-detail", kwargs={"pk": self.carSale.id})

        payload = {"price": 60_000, "recycle": 10_000, "status": True}
        response = self.client.patch(self.url, payload)
        self.carSale.refresh_from_db()
        self.assertEqual(response.data["price"], 60_000)
        self.assertEqual(response.data["recycle"], 10_000)
        self.assertEqual(response.data["status"], True)