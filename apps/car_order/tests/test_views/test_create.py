from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from auction.models import Auction
from authorization.models import User
from car_model.models import CarMark
from car_order.models import CarOrder
from transport_companies.models import TransportCompany
from utils.tests import Authenticate

from django.conf import settings


class TestCreateAPIView(Authenticate, APITestCase):
    def setUp(self):
        self.url = reverse("car-order-list-create")
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
        self.sanri = User.objects.create_user(
            password="123",
            fullName="My owner client",
            country="KG",
            email="ownerclient@gmail.com",
            phoneNumber="+996771221103",
            service=User.SERVICE_ENTIRE,
            atWhatPrice=User.AT_WHAT_PRICE_BY_FOB,
            username=settings.SANRI_USERNAME,
            sizeFOB=25000,
        )
        self.token = self.create_token(self.user)

        self.auction = Auction.objects.create(
            name="MyTestAuction",
            parkingPrice1=25000,
            parkingPrice2=25000,
            parkingPrice3=25000,
            parkingPrice4=25000,
        )

        self.car_marks = {"honda": CarMark.objects.create(name="HONDA")}
        self.car_models = {
            "fit": self.car_marks["honda"].models.create(name="FIT")
        }

        self.transport_company = TransportCompany.objects.create(
            name="MyTestTransportCompany"
        )

    def test_create_api_view(self):
        """
        Test logic works correct when creating new CarOrder instance
        """

        self.set_credentials(self.token)

        payload = {
            "client_id": self.user.id,
            "auction_id": self.auction.id,
            "carModel_id": self.car_models["fit"].id,
            "documentsGiven": True,
            "vinNumber": "xs-500",
            "year": "2003",
            "price": 25000,
            "recycle": 2000,
            "auctionFees": 250,
            "transport": 21000,
            "amount": 250,
            "carNumber": "removed",
            "created_at": "2003-11-22",
            "transportCompany_id": self.transport_company.id,
            "additional_expenses": 100,
            "comment": "mycarordercomment",
            "fob": 12000
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "CarOrder was not created successfully",
        )

        self.car_order = CarOrder.objects.get(id=response.data["id"])

        self.user.refresh_from_db()
        self.assertEqual(
            self.user.balance.amount,
            -self.car_order.withdrawal.balance.sum_in_jpy,
        )
        self.assertEqual(self.sanri.balance.amount, 0)

    def test_create_with_user_fob2(self):
        self.set_credentials(self.token)

        self.user.atWhatPrice = self.user.AT_WHAT_PRICE_BY_FOB2
        self.user.save()
        self.user.refresh_from_db()

        payload = {
            "client_id": self.user.id,
            "auction_id": self.auction.id,
            "carModel_id": self.car_models["fit"].id,
            "documentsGiven": True,
            "vinNumber": "xs-500",
            "year": "2003",
            "price": 25000,
            "recycle": 2000,
            "auctionFees": 250,
            "transport": 21000,
            "amount": 250,
            "carNumber": "removed",
            "created_at": "2003-11-22",
            "transportCompany_id": self.transport_company.id,
            "additional_expenses": 100,
            "comment": "mycarordercomment",
            "fob": 12000
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.car_order = CarOrder.objects.get(id=response.data["id"])

        self.assertEqual(
            self.sanri.balance.amount,
            -(self.car_order.recycle + self.car_order.price * 0.1),
        )

    def test_create_with_no_authtoken(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
