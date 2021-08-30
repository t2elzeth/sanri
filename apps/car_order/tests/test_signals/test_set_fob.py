from django.test import TestCase

from car_order.models import CarOrder
from authorization.models import User
from auction.models import Auction
from car_model.models import CarMark, CarModel
from transport_companies.models import TransportCompany


class TestSetFOB(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            password="123",
            fullName="My owner client",
            country="KG",
            email="ownerclient@gmail.com",
            phoneNumber="+996771221103",
            service=User.SERVICE_ENTIRE,
            atWhatPrice=User.AT_WHAT_PRICE_BY_FOB,
            username="client_by_fob",
            sizeFOB=25000,
        )

        self.auction = Auction.objects.create(
            name='MyTestAuction',
            parkingPrice1=25000,
            parkingPrice2=25000,
            parkingPrice3=25000,
            parkingPrice4=25000
        )

        self.car_marks = {
            'honda': CarMark.objects.create(
                name="HONDA"
            )
        }
        self.car_models = {
            'fit': self.car_marks['honda'].models.create(
                name="FIT"
            )
        }

        self.transport_company = TransportCompany.objects.create(
            name="MyTestTransportCompany"
        )

        self.car_order = CarOrder.objects.create(
            client=self.user,
            auction=self.auction,
            lotNumber=10000,
            carModel=self.car_models['fit'],
            vinNumber="vx-1000",
            year=2015,
            price=20000,
            recycle=10000,
            auctionFees=20000,
            transport=25000,
            amount=2,
            transportCompany=self.transport_company,
            carNumber=CarOrder.CAR_NUMBER_REMOVED,
            documentsGiven=False
        )

    def test_fob_when_created(self):
        """
        Test if fob is set to client's sizeFOB
        when CarOrder instance is newly created
        """
        self.assertEqual(self.car_order.fob, self.user.sizeFOB)

    def test_user_sizeFOB_changed(self):
        """
        Test if CarOrder's fob gets updated as client's fob changes
        """
        self.user.sizeFOB = 15000
        self.user.save()

        self.car_order.refresh_from_db()
        self.assertEqual(self.car_order.fob, self.user.sizeFOB)
