from auction.models import Auction
from authorization.models import Balance, User
from car_model.models import CarMark
from car_order.formulas import calculate_total, calculate_total_fob
from car_order.models import CarOrder
from car_resale.models import CarResale
from car_sale.models import CarSale
from django.conf import settings
from income.models import IncomeType
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from transport_companies.models import TransportCompany

from utils.tests import Authenticate


class CreateNewCarResaleTest(Authenticate, APITestCase):
    def setUp(self) -> None:
        self.url = reverse("car-resale-list-create")
        self.oldClient = User.objects.create_user(
            password="123",
            fullName="My owner client",
            country="KG",
            email="oldClient@gmail.com",
            phoneNumber="+996771221103",
            service=User.SERVICE_ENTIRE,
            atWhatPrice=User.AT_WHAT_PRICE_BY_FACT,
            username="owner_client",
        )
        self.token = self.create_token(self.oldClient)

        self.newClient = User.objects.create_user(
            password="123",
            fullName="My new client",
            country="KG",
            email="newclient@gmail.com",
            phoneNumber="+996771221103",
            service=User.SERVICE_ENTIRE,
            atWhatPrice=User.AT_WHAT_PRICE_BY_FACT,
            username="new_client",
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
        self.transport_company = TransportCompany.objects.create(
            name="My transport company"
        )

        self.carOrder = CarOrder.objects.create(
            client=self.oldClient,
            auction=self.auction,
            lotNumber=25000,
            carModel=self.car_model,
            vinNumber=25000,
            year=2019,
            fob=self.oldClient.sizeFOB,
            price=50000,
            recycle=20000,
            auctionFees=25000,
            transport=3000,
            carNumber=CarOrder.CAR_NUMBER_NOT_GIVEN,
            transportCompany=self.transport_company,
        )

    def _make_request_and_get_car_resale_object(self):
        self.set_credentials(self.token)
        self.sale_price = self.carOrder.price + 20000
        payload = {
            "oldClient_id": self.oldClient.id,
            "newClient_id": self.newClient.id,
            "carOrder_id": self.carOrder.id,
            "startingPrice": self.carOrder.price,
            "salePrice": self.sale_price,
        }
        response = self.client.post(self.url, payload)

        self.carResale = CarResale.objects.get(id=response.data["id"])

    def _check_car_order(self):
        self.carOrder.refresh_from_db()
        new_total = calculate_total(
            self.carOrder.price,
            self.carOrder.auctionFees,
            self.carOrder.recycle,
            self.carOrder.transport,
        )
        new_total_fob = calculate_total_fob(
            self.carOrder.price,
            self.carOrder.amount,
            self.carOrder.transport,
            self.carOrder.fob,
        )

        # Set new owner of carOrder
        self.assertEqual(self.carOrder.client, self.newClient)

        # Set new price of carOrder
        self.assertEqual(self.carOrder.price, self.sale_price)

        # New client doesn't work by fob, so amount is 0
        self.assertEqual(self.carOrder.amount, 0)

        # Set new client's fob
        self.assertEqual(self.carOrder.fob, self.newClient.sizeFOB)

        # Recalculate total
        self.assertEqual(self.carOrder.total, new_total)
        # Recalculate total FOB
        self.assertEqual(self.carOrder.total_FOB, new_total_fob)

    def check_balance_action(self):
        self.assertTrue(
            Balance.objects.filter(
                client=self.oldClient,
                sum_in_jpy=self.carOrder.total,
                rate=1,
                sum_in_usa=self.carOrder.total,
                balance_action=Balance.BALANCE_ACTION_REPLENISHMENT,
            ).exists()
        )

        # Add balance withdrawal for new client
        self.assertTrue(
            Balance.objects.filter(
                client=self.newClient,
                sum_in_jpy=self.carOrder.total,
                rate=1,
                sum_in_usa=self.carOrder.total,
                balance_action=Balance.BALANCE_ACTION_WITHDRAWAL,
            ).exists()
        )

    def _check_car_sales_deletion(self):
        self.assertFalse(
            CarSale.objects.filter(carOrder=self.carOrder).exists()
        )

    def test_create_new_car_resale_sell_to_user_working_by_fact(self):
        self._make_request_and_get_car_resale_object()
        self._check_car_order()
        self.check_balance_action()
        self._check_car_sales_deletion()

    def test_create_new_car_resale_sell_to_user_working_by_fob(self):
        self.newClient.sizeFOB = 65000
        self.newClient.atWhatPrice = User.AT_WHAT_PRICE_BY_FOB
        self.newClient.save()

        self._make_request_and_get_car_resale_object()
        self._check_car_order()
        self.check_balance_action()
        self._check_car_sales_deletion()

    def test_create_new_car_resale_as_sanrijp(self):
        self.oldClient.username = settings.SANRI_USERNAME
        self.oldClient.sizeFOB = 0
        self.oldClient.atWhatPrice = User.AT_WHAT_PRICE_BY_FACT
        self.oldClient.save()

        self._make_request_and_get_car_resale_object()
        self._check_car_order()
        self.check_balance_action()
        self._check_car_sales_deletion()

        income_type = IncomeType.objects.get(name="car_resale")
        self.assertTrue(
            income_type.incomes.filter(
                amount=self.carResale.salePrice - self.carResale.startingPrice
            ).exists()
        )
