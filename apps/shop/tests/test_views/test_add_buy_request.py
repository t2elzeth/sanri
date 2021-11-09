from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from authorization.models import User
from authorization.tests.factory import ClientFactory
from shop.models_factory import CarFactory
from utils.tests import Authenticate


class TestAddCarView(APITestCase, Authenticate):
    def setUp(self) -> None:
        self.user: User = ClientFactory.create()
        self.token = self.user.login()
        self.car = CarFactory.create()
        self.url = reverse("shop-buy-request-add")

    def test_view(self):
        self.set_credentials(self.token)

        payload = {
            "car_id": self.car.id,
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
