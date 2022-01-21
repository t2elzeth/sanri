from auction.models import Auction
from authorization.models import User
from car_model.models import CarMark
from car_order.models import CarOrder
from car_sale.formulas import calculate_total
from car_sale.models import CarSale
from django.test import TestCase
from transport_companies.models import TransportCompany


class CreateCarSale(TestCase):
    def setUp(self) -> None:
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

        self.car_sale = CarSale.objects.create(
            ownerClient=self.ownerClient,
            auction=self.auction,
            carOrder=self.carOrder,
            auctionFees=25000,
            salesFees=25000,
        )

    def test_try_to_change_price_with_status_false(self):
        self.car_sale.status = False
        self.car_sale.save()

        self.assertEqual(self.car_sale.price, 0)
        self.assertEqual(self.car_sale.recycle, 0)

        self.car_sale.price = 60000
        self.car_sale.recycle = 20000
        self.car_sale.save()

        self.assertEqual(self.car_sale.price, 0)
        self.assertEqual(self.car_sale.recycle, 0)

        new_total = calculate_total(
            self.car_sale.price,
            self.car_sale.recycle,
            self.car_sale.auctionFees,
            self.car_sale.salesFees,
        )
        self.assertEqual(self.car_sale.total, new_total)

    def test_try_to_change_price_and_recycle_with_status_true(self):
        self.car_sale.status = True
        self.car_sale.save()
        self.car_sale.refresh_from_db()

        self.assertEqual(self.car_sale.price, 0)
        self.assertEqual(self.car_sale.recycle, 0)

        self.car_sale.price = 60000
        self.car_sale.recycle = 20000
        self.car_sale.save()

        self.assertEqual(self.car_sale.price, 60000)
        self.assertEqual(self.car_sale.recycle, 20000)

        new_total = calculate_total(
            self.car_sale.price,
            self.car_sale.recycle,
            self.car_sale.auctionFees,
            self.car_sale.salesFees,
        )
        self.assertEqual(self.car_sale.total, new_total)

        # Make sure carOrder is deleted
        self.assertIsNotNone(self.car_sale.carOrder)
