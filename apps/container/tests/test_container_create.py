from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from auction.models import Auction
from authorization.models import User
from car_model.models import CarMark
from car_order.models import CarOrder
from container.formulas import calculate_total
from container.models import Container


class CreateContainerTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("container-list-create")
        self.container_client = User.objects.create_user(
            password="123",
            fullName="My owner client",
            country="KG",
            email="oldClient@gmail.com",
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
        self.car_model_FIT = self.car_mark.models.create(name="FIT")
        self.car_model_ODYSSEI = self.car_mark.models.create(name="ODYSSEI")

        self.carOrder_1 = CarOrder.objects.create(
            client=self.container_client,
            auction=self.auction,
            lotNumber=25000,
            carModel=self.car_model_FIT,
            vinNumber=25000,
            year=2019,
            fob=self.container_client.sizeFOB,
            price=50000,
            recycle=20000,
            auctionFees=25000,
            transport=3000,
            carNumber=CarOrder.CAR_NUMBER_NOT_GIVEN,
        )

        self.carOrder_2 = CarOrder.objects.create(
            client=self.container_client,
            auction=self.auction,
            lotNumber=25000,
            carModel=self.car_model_ODYSSEI,
            vinNumber=25000,
            year=2019,
            fob=self.container_client.sizeFOB,
            price=50000,
            recycle=20000,
            auctionFees=25000,
            transport=3000,
            carNumber=CarOrder.CAR_NUMBER_NOT_GIVEN,
        )

    def test_container_create_with_valid_data(self):
        payload = {
            "client_id": self.container_client.id,
            "name": "My test container",
            "dateOfSending": "2003-11-22",
            "commission": 2500,
            "containerTransportation": 2500,
            "packagingMaterials": 2500,
            "transportation": 2000,
            "loading": 2000,
            "wheelRecycling": {"count": 25, "sum": 200},
            "wheelSales": {"count": 20, "sum": 2000},
            "status": Container.STATUS_GOING_TO,
            "car_ids": [self.car_model_FIT.id, self.car_model_ODYSSEI.id],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        container = Container.objects.get(id=response.data["id"])
        wheel_recycling = container.wheel_recycling
        wheel_sales = container.wheel_sales
        self.assertEqual(wheel_recycling.count, 25)
        self.assertEqual(wheel_recycling.sum, 200)
        self.assertEqual(wheel_sales.count, 20)
        self.assertEqual(wheel_sales.sum, 2000)
        self.assertEqual(container.totalAmount, calculate_total(
            container.commission,
            container.containerTransportation,
            container.packagingMaterials,
            wheel_recycling.sum,
            wheel_sales.sum
        ))
        print('This is cars list: ', response.data['cars'])
        self.assertEqual(len(response.data['cars']), 2)

        response = self.client.patch(f'/api/Container/{container.id}/', {'packagingMaterials': 287, 'wheelSales': {
            'count': 259
        }, 'car_ids': [self.car_model_FIT.id]}, format='json')
        self.assertEqual(response.data['packagingMaterials'], 287)
        self.assertEqual(len(response.data['cars']), 1)
