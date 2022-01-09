from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from authorization.models import User
from authorization.tests.factory import ClientFactory
from car_model.tests.factory import CarModelFactory
from utils.tests import Authenticate


class TestAddCarView(APITestCase, Authenticate):
    AUTHENTICATION_CREDENTIALS = "Token {}"

    def setUp(self) -> None:
        self.user: User = ClientFactory.create()
        self.token = self.user.login()
        self.model = CarModelFactory.create()
        self.url = reverse("shop-car-add")

    def test_view(self):
        self.set_credentials(self.token)

        payload = {
            "model_id": 1,
            "year": 2003,
            "volume": 4.5,
            "mileage": 195_000.45,
            "condition": 4,
            "price": 25000,
            "description": "The best car you have ever seen",
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
