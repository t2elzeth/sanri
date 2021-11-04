from django.conf import settings
from django.test import TestCase

from authorization.models import User
from car_order.models import CarOrder
from car_order.tests.factory import CarOrderFactory, ClientFactory
from car_order import formulas


class TestCalculateTotalFactClient(TestCase):
    def setUp(self) -> None:
        self.client: User = ClientFactory.create(atWhatPrice=User.AT_WHAT_PRICE_BY_FACT)
        self.order: CarOrder = CarOrderFactory.create(
            client=self.client,
        )

    def test_total(self):
        result = self.order.total
        expected = formulas.calculate_total(
            self.order.price,
            self.order.auctionFees,
            self.order.recycle,
            self.order.transport
        )

        self.assertEqual(result, expected)

    def test_total_FOB(self):
        result = self.order.total_FOB
        expected = 0

        self.assertEqual(result, expected)

    def test_total_FOB2(self):
        result = self.order.total_FOB2
        expected = 0

        self.assertEqual(result, expected)


class TestCalculateTotalFOBClient(TestCase):
    def setUp(self) -> None:
        self.client: User = ClientFactory.create(atWhatPrice=User.AT_WHAT_PRICE_BY_FOB)
        self.order: CarOrder = CarOrderFactory.create(client=self.client)

    def test_total(self):
        result = self.order.total
        expected = formulas.calculate_total(
            self.order.price,
            self.order.auctionFees,
            self.order.recycle,
            self.order.transport
        )

        self.assertEqual(result, expected)

    def test_total_FOB(self):
        result = self.order.total_FOB
        expected = formulas.calculate_total_fob(
            self.order.price,
            self.order.amount,
            self.order.transport,
            self.order.fob
        )

        self.assertEqual(result, expected)

    def test_total_FOB2(self):
        result = self.order.total_FOB2
        expected = 0

        self.assertEqual(result, expected)


class TestCalculateTotalFOB2Client(TestCase):
    def setUp(self) -> None:
        ClientFactory.create(username=settings.SANRI_USERNAME)
        self.client: User = ClientFactory.create(atWhatPrice=User.AT_WHAT_PRICE_BY_FOB2)
        self.order: CarOrder = CarOrderFactory.create(client=self.client)

    def test_total(self):
        result = self.order.total
        expected = formulas.calculate_total(
            self.order.price,
            self.order.auctionFees,
            self.order.recycle,
            self.order.transport
        )

        self.assertEqual(result, expected)

    def test_total_FOB(self):
        result = self.order.total_FOB
        expected = 0

        self.assertEqual(result, expected)

    def test_total_FOB2(self):
        result = self.order.total_FOB2
        expected = formulas.calculate_total_fob2(
            self.order.price,
            self.order.auctionFees,
            self.order.transport,
            self.order.fob
        )

        self.assertEqual(result, expected)
