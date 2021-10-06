from django.test import TestCase

from auction.models import Auction
from authorization.models import User
from car_model.models import CarMark
from car_model.tests.factory import CarMarkFactory
from car_order.models import CarOrder
from transport_companies.models import TransportCompany
from .factory import CarOrderFactory, ClientFactory, AuctionFactory, TransportCompanyFactory


class TestCarOrderAndUserRelation(TestCase):
    def setUp(self) -> None:
        self.user = ClientFactory.create(sizeFOB=25000)
        self.auction = AuctionFactory.create()
        self.car_marks = {"honda": CarMarkFactory.create(name="HONDA")}
        self.car_models = {
            "fit": self.car_marks["honda"].models.create(name="FIT")
        }
        self.transport_company = TransportCompanyFactory.create()
        self.car_order = CarOrderFactory.create(client=self.user)

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

    def test_get_total(self):
        # Check when user works by FACT
        self.user.atWhatPrice = self.user.AT_WHAT_PRICE_BY_FACT
        self.user.save()
        self.car_order.refresh_from_db()
        self.assertEqual(self.car_order.total, self.car_order.get_total())

        # Check when user works by FOB
        self.user.atWhatPrice = self.user.AT_WHAT_PRICE_BY_FOB
        self.user.save()
        self.car_order.refresh_from_db()
        self.assertEqual(self.car_order.total_FOB, self.car_order.get_total())

        # Check when user works by FOB2
        self.user.atWhatPrice = self.user.AT_WHAT_PRICE_BY_FOB2
        self.user.save()
        self.car_order.refresh_from_db()
        self.assertEqual(self.car_order.total_FOB2, self.car_order.get_total())


class TestCarOrderBalanceWithdrawal(TestCase):
    def setUp(self) -> None:
        self.user = ClientFactory.create(sizeFOB=25000)

        self.auction = AuctionFactory.create()

        self.car_marks = {"honda": CarMarkFactory.create(name="HONDA")}
        self.car_models = {
            "fit": self.car_marks["honda"].models.create(name="FIT")
        }

        self.transport_company = TransportCompanyFactory.create()

        self.car_order = CarOrderFactory.create(client=self.user)
        self.withdrawal = self.car_order.withdrawal

    def test_initial_car_order_withdrawal_amount(self):
        """
        Make sure the BalanceWithdrawal amount is correct
        when new instance of CarOrder created
        """
        self.assertEqual(
            self.withdrawal.balance.sum_in_jpy, self.car_order.get_total()
        )

    def test_car_order_total_changes(self):
        self.car_order.price = 250000
        self.car_order.save()

        self.withdrawal.refresh_from_db()
        self.assertEqual(
            self.withdrawal.balance.sum_in_jpy, self.car_order.get_total()
        )
