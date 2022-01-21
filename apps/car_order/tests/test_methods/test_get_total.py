from authorization.models import User
from car_order.models import CarOrder
from car_order.tests.factory import CarOrderFactory, ClientFactory
from django.conf import settings
from django.test import TestCase


class TestGetTotalFactClient(TestCase):
    def setUp(self) -> None:
        self.client: User = ClientFactory.create(
            atWhatPrice=User.AT_WHAT_PRICE_BY_FACT
        )
        self.order: CarOrder = CarOrderFactory.create(client=self.client)

    def test_get_total(self):
        total = self.order.get_total()
        self.assertEqual(total, self.order.total)


class TestGetTotalFOBClient(TestCase):
    def setUp(self) -> None:
        self.client: User = ClientFactory.create(
            atWhatPrice=User.AT_WHAT_PRICE_BY_FOB
        )
        self.order: CarOrder = CarOrderFactory.create(client=self.client)

    def test_get_total(self):
        total = self.order.get_total()

        self.assertEqual(total, self.order.total_FOB)


class TestGetTotalFOB2Client(TestCase):
    def setUp(self) -> None:
        ClientFactory.create(username=settings.SANRI_USERNAME)
        self.client: User = ClientFactory.create(
            atWhatPrice=User.AT_WHAT_PRICE_BY_FOB2
        )
        self.order: CarOrder = CarOrderFactory.create(client=self.client)

    def test_get_total(self):
        total = self.order.get_total()

        self.assertEqual(total, self.order.total_FOB2)
