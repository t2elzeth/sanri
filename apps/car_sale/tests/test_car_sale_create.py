from auction.models import Auction
from authorization.models import Balance, User
from car_model.models import CarMark
from car_order.models import CarOrder, BalanceWithdrawal as CarOrderWithdrawal
from car_sale.models import CarSale
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from transport_companies.models import TransportCompany

from utils.tests import Authenticate


class TestCreateNewCarSale(Authenticate, APITestCase):
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
        self.token = self.create_token(self.ownerClient)

        self.auction = Auction.objects.create(
            name="AuctionName",
            parkingPrice1=25000,
            parkingPrice2=20000,
            parkingPrice3=15000,
            parkingPrice4=10000,
        )

        self.car_mark = CarMark.objects.create(name="HONDA")
        self.car_model = self.car_mark.models.create(name="FIT")
        self.transport_company = TransportCompany.objects.create(
            name="My transport company"
        )

        self.carOrder = CarOrder.objects.create(
            client=self.ownerClient,
            auction=self.auction,
            lotNumber=25000,
            carModel=self.car_model,
            vinNumber=25000,
            year=2019,
            price=50000,
            recycle=20000,
            auctionFees=25000,
            transport=3000,
            carNumber=CarOrder.CAR_NUMBER_NOT_GIVEN,
            transportCompany=self.transport_company,
        )

        self.carSale = CarSale.objects.create(
            ownerClient=self.ownerClient,
            auction=self.auction,
            carOrder=self.carOrder,
            auctionFees=25000,
            salesFees=25000,
        )

    def test_create(self):
        self.set_credentials(self.token)
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

        self.assertEqual(self.carSale.ownerClient, self.carOrder.client)
        payload = {"price": 60_000, "recycle": 10_000, "status": True}
        response = self.client.patch(self.url, payload)

        car_order_withdrawal = self.carOrder.withdrawal
        car_order_carModel = str(self.carOrder.carModel)
        car_order_vinNumber = str(self.carOrder.vinNumber)

        self.carSale.refresh_from_db()
        self.assertTrue(self.carSale.carOrder.is_sold)
        self.assertEqual(response.data["price"], 60_000)
        self.assertEqual(response.data["recycle"], 10_000)
        self.assertEqual(response.data["status"], True)
        self.assertTrue(
            Balance.objects.filter(
                client=self.carSale.ownerClient,
                sum_in_jpy=self.carSale.total,
                payment_type=Balance.PAYMENT_TYPE_CASHLESS,
                balance_action=Balance.BALANCE_ACTION_REPLENISHMENT,
            ).exists()
        )

        # Check if balance withdrawal for CarOrder is kept
        car_order_withdrawal.refresh_from_db()
        self.assertTrue(
            CarOrderWithdrawal.objects.filter(
                id=car_order_withdrawal.id
            ).exists()
        )
        self.assertEqual(
            car_order_withdrawal.balance.sum_in_jpy, self.carOrder.total
        )

        # Check if carOrder data is kept
        self.assertEqual(self.carSale.vinNumber, car_order_vinNumber)
        self.assertEqual(self.carSale.carModel, car_order_carModel)

    def test_update_set_to_true_with_no_price_and_recycle(self):
        self.url = reverse("car-sale-detail", kwargs={"pk": self.carSale.id})

        # Empty payload
        payload = {"status": True}
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Half empty payload
        payload = {"status": True, "price": 25000}
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {"status": True, "recycle": 5000}
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
