from django.test import TestCase

from car_order.formulas import (
    calculate_total,
    calculate_total_fob,
    calculate_total_fob2,
    get_transport,
    MIN_TRANSPORT_TO_INCLUDE,
)


class TestGetTransportFormula(TestCase):
    def setUp(self) -> None:
        self.formula = get_transport

    def test_min_transport_to_include(self):
        expected = 6000
        self.assertEqual(expected, MIN_TRANSPORT_TO_INCLUDE)

    def test_transport_gt_min_transport(self):
        given_transport = 7000
        transport = self.formula(given_transport)

        self.assertEqual(transport, given_transport)

    def test_transport_eq_min_transport(self):
        given_transport = 6000
        transport = self.formula(given_transport)

        self.assertEqual(transport, 0)

    def test_transport_lt_min_transport(self):
        given_transport = 5000
        transport = self.formula(given_transport)

        self.assertEqual(transport, 0)


class TestCalculateTotalFormula(TestCase):
    def setUp(self) -> None:
        self.formula = calculate_total

        self.kwargs = {
            "price": 25_000,
            "auctionFees": 10_000,
            "recycle": 100,
            "transport": 3_000,
        }

    def test_calculate_total(self):
        result = self.formula(**self.kwargs)

        expected = 25_000 + 2500 + 10_000 + 100 + 3_000

        self.assertEqual(result, expected)


class TestCalculateTotalFOBFormula(TestCase):
    def setUp(self) -> None:
        self.formula = calculate_total_fob

        self.price = 25_000
        self.amount = 100
        self.fob = 1_000

    def get_kwargs(self, transport):
        return {
            "price": self.price,
            "amount": self.amount,
            "fob": self.fob,
            "transport": transport,
        }

    def test_transport_lt_min_transport(self):
        transport = MIN_TRANSPORT_TO_INCLUDE - 1000
        kwargs = self.get_kwargs(transport)

        result = self.formula(**kwargs)
        expected = self.price + self.amount + self.fob

        self.assertEqual(result, expected)

    def test_transport_gt_min_transport(self):
        transport = MIN_TRANSPORT_TO_INCLUDE + 1000
        kwargs = self.get_kwargs(transport)

        result = self.formula(**kwargs)
        expected = self.price + self.amount + self.fob + transport

        self.assertEqual(result, expected)

    def test_transport_eq_min_transport(self):
        transport = MIN_TRANSPORT_TO_INCLUDE
        kwargs = self.get_kwargs(transport)

        result = self.formula(**kwargs)
        expected = self.price + self.amount + self.fob

        self.assertEqual(result, expected)


class TestCalculateTotalFOB2Formula(TestCase):
    def setUp(self) -> None:
        self.price = 25_000
        self.auctionFees = 100
        self.fob = 1_000
        self.formula = calculate_total_fob2

    def get_kwargs(self, transport):
        return {
            "price": self.price,
            "auctionFees": self.auctionFees,
            "fob": self.fob,
            "transport": transport,
        }

    def test_transport_lt_min_transport(self):
        transport = MIN_TRANSPORT_TO_INCLUDE - 1000
        kwargs = self.get_kwargs(transport)

        result = self.formula(**kwargs)
        expected = self.price + self.auctionFees + self.fob

        self.assertEqual(result, expected)

    def test_transport_gt_min_transport(self):
        transport = MIN_TRANSPORT_TO_INCLUDE + 1000
        kwargs = self.get_kwargs(transport)

        result = self.formula(**kwargs)
        expected = self.price + self.auctionFees + self.fob + transport

        self.assertEqual(result, expected)

    def test_transport_eq_min_transport(self):
        transport = MIN_TRANSPORT_TO_INCLUDE
        kwargs = self.get_kwargs(transport)

        result = self.formula(**kwargs)
        expected = self.price + self.auctionFees + self.fob

        self.assertEqual(result, expected)
