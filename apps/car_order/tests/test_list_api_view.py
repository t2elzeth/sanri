from auction.models import Auction
from authorization.models import User
from car_model.models import CarMark
from car_order.models import CarOrder
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from transport_companies.models import TransportCompany


class TestGetListOfCarOrdersAsClient(APITestCase):
    AUTHENTICATION_CREDENTIALS = "Token {}"

    def setUp(self) -> None:
        self.url = reverse("car-order-list-create")
        self.ownerClient = User.objects.create_user(
            password="123",
            fullName="My owner client",
            country="KG",
            email="oldClient@gmail.com",
            phoneNumber="+996771221103",
            service=User.SERVICE_ENTIRE,
            atWhatPrice=User.AT_WHAT_PRICE_BY_FACT,
            username="owner_client",
            user_type=User.USER_TYPE_CLIENT,
        )
        self.notOwnerClient = User.objects.create_user(
            password="123",
            fullName="My owner client",
            country="KG",
            email="oldClient@gmail.com",
            phoneNumber="+996771221103",
            service=User.SERVICE_ENTIRE,
            atWhatPrice=User.AT_WHAT_PRICE_BY_FACT,
            username="not_owner_client",
            user_type=User.USER_TYPE_CLIENT,
        )
        self.manager = User.objects.create_user(
            password="123",
            fullName="My owner client",
            country="KG",
            email="oldClient@gmail.com",
            phoneNumber="+996771221103",
            service=User.SERVICE_ENTIRE,
            atWhatPrice=User.AT_WHAT_PRICE_BY_FACT,
            username="manager",
            user_type=User.USER_TYPE_EMPLOYEE,
        )

        self.ownerClient_token = Token.objects.create(user=self.ownerClient)
        self.notOwnerClient_token = Token.objects.create(
            user=self.notOwnerClient
        )
        self.manager_token = Token.objects.create(user=self.manager)

        self.auction = Auction.objects.create(
            name="AuctionName",
            parkingPrice1=25000,
            parkingPrice2=20000,
            parkingPrice3=15000,
            parkingPrice4=10000,
        )

        self.car_mark_HONDA = CarMark.objects.create(name="HONDA")
        self.car_model_FIT = self.car_mark_HONDA.models.create(name="FIT")
        self.car_model_ACCORD = self.car_mark_HONDA.models.create(
            name="Accord"
        )

        self.transportCompany = TransportCompany.objects.create(
            name="Mytransportcompany"
        )

        self.carOrder_FIT = CarOrder.objects.create(
            client=self.ownerClient,
            auction=self.auction,
            lotNumber=25000,
            carModel=self.car_model_FIT,
            vinNumber=25000,
            year=2019,
            fob=self.ownerClient.sizeFOB,
            price=50000,
            recycle=20000,
            auctionFees=25000,
            transport=3000,
            carNumber=CarOrder.CAR_NUMBER_NOT_GIVEN,
            transportCompany=self.transportCompany,
        )

        self.carOrder_FIT = CarOrder.objects.create(
            client=self.ownerClient,
            auction=self.auction,
            lotNumber=25000,
            carModel=self.car_model_ACCORD,
            vinNumber=25000,
            year=2019,
            fob=self.ownerClient.sizeFOB,
            price=50000,
            recycle=20000,
            auctionFees=25000,
            transport=3000,
            carNumber=CarOrder.CAR_NUMBER_NOT_GIVEN,
            transportCompany=self.transportCompany,
        )

        self.carOrder_FIT = CarOrder.objects.create(
            client=self.notOwnerClient,
            auction=self.auction,
            lotNumber=25000,
            carModel=self.car_model_FIT,
            vinNumber=25000,
            year=2019,
            fob=self.notOwnerClient.sizeFOB,
            price=50000,
            recycle=20000,
            auctionFees=25000,
            transport=3000,
            carNumber=CarOrder.CAR_NUMBER_NOT_GIVEN,
            transportCompany=self.transportCompany,
        )

    def test_get_list_of_car_orders(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.AUTHENTICATION_CREDENTIALS.format(
                self.ownerClient_token
            )
        )

        response = self.client.get(self.url)

        print(len(response.data))

        self.client.credentials(
            HTTP_AUTHORIZATION=self.AUTHENTICATION_CREDENTIALS.format(
                self.manager_token
            )
        )
        response = self.client.get(self.url)

        print(len(response.data))
