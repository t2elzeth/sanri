from django.test import TestCase
from django.conf import settings
from authorization.models import Balance
from car_model.tests.factory import CarMarkFactory
from .factory import (
    CarOrderFactory,
    ClientFactory,
    AuctionFactory,
    TransportCompanyFactory,
)


class TestCarOrderAndUserRelation(TestCase):
    def setUp(self) -> None:
        self.user = ClientFactory.create(sizeFOB=25000)
        self.sanri = ClientFactory.create(username=settings.SANRI_USERNAME)
        self.order = CarOrderFactory.create(client=self.user, fob=12000)

    def test_create_order_for_fact_client(self):
        """
        Create order for fact client
        """
        if not self.user.works_by.by_fact:
            self.user.atWhatPrice = self.user.AT_WHAT_PRICE_BY_FACT
            self.user.save()

        self.order = CarOrderFactory.create(client=self.user)
        balance_record = self.user.balances.filter(
            client=self.user,
            sum_in_jpy=self.order.get_total(),
            balance_action=Balance.BALANCE_ACTION_WITHDRAWAL,
        ).first()
        self.assertIsNotNone(balance_record)

    def test_create_order_for_fob2_client(self):
        """Create order for fob2 client"""
        if not self.user.works_by.by_fob2:
            self.user.atWhatPrice = self.user.AT_WHAT_PRICE_BY_FOB2
            self.user.save()

        self.order = CarOrderFactory.create(client=self.user)
        balance_record = self.sanri.balances.filter(
            client=self.sanri,
            sum_in_jpy=self.order.recycle + self.order.price * 0.1,
            balance_action=Balance.BALANCE_ACTION_WITHDRAWAL,
        ).first()
        self.assertIsNotNone(
            balance_record, "Balance record for sanri user was not created"
        )

        balance_record = self.user.balances.filter(
            client=self.user,
            sum_in_jpy=self.order.get_total(),
            balance_action=Balance.BALANCE_ACTION_WITHDRAWAL,
        )
        self.assertIsNotNone(balance_record)

    def test_fob_when_created(self):
        """
        Test if fob is set correctly when new instance is created
        """
        self.assertEqual(self.order.fob, 12000)

        self.user.sizeFOB = 10000
        self.user.save()

        self.order.refresh_from_db()
        self.assertEqual(self.order.fob, 12000)

    def test_balance_client_changes_when_car_order_client_changed(self):
        """
        Try to change the client of order and see
        if balance record is reassignled to a new client as well
        """

        self.user = ClientFactory.create()
        self.order.client = self.user
        self.order.save()
        balance_record = self.user.balances.filter(
            client=self.user,
            sum_in_jpy=self.order.get_total(),
            balance_action=Balance.BALANCE_ACTION_WITHDRAWAL,
        ).first()

        self.assertEqual(self.order.client.id, self.user.id)
        self.assertEqual(self.order.withdrawal.balance.client.id, self.user.id)
        self.assertEqual(balance_record.client.id, self.user.id)

    def test_user_sizeFOB_changed(self):
        """
        Test if CarOrder's fob gets updated as client's fob changes
        """
        self.user.sizeFOB = 15000
        self.user.save()

        self.order.refresh_from_db()
        self.assertEqual(self.order.fob, self.user.sizeFOB)

    def test_get_total(self):
        # Check when user works by FACT
        self.user.atWhatPrice = self.user.AT_WHAT_PRICE_BY_FACT
        self.user.save()
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, self.order.get_total())

        # Check when user works by FOB
        self.user.atWhatPrice = self.user.AT_WHAT_PRICE_BY_FOB
        self.user.save()
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_FOB, self.order.get_total())

        # Check when user works by FOB2
        self.user.atWhatPrice = self.user.AT_WHAT_PRICE_BY_FOB2
        self.user.save()
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_FOB2, self.order.get_total())


class TestCarOrderBalanceWithdrawal(TestCase):
    def setUp(self) -> None:
        self.user = ClientFactory.create(sizeFOB=25000)

        self.auction = AuctionFactory.create()

        self.car_marks = {"honda": CarMarkFactory.create(name="HONDA")}
        self.car_models = {
            "fit": self.car_marks["honda"].models.create(name="FIT")
        }

        self.transport_company = TransportCompanyFactory.create()

        self.order = CarOrderFactory.create(client=self.user)
        self.withdrawal = self.order.withdrawal

    def test_initial_car_order_withdrawal_amount(self):
        """
        Make sure the BalanceWithdrawal amount is correct
        when new instance of CarOrder created
        """
        self.assertEqual(
            self.withdrawal.balance.sum_in_jpy, self.order.get_total()
        )

    def test_car_order_total_changes(self):
        self.order.price = 250000
        self.order.save()

        self.withdrawal.refresh_from_db()
        self.assertEqual(
            self.withdrawal.balance.sum_in_jpy, self.order.get_total()
        )

    def test_withdrawal_delete(self):
        balance_record = self.withdrawal.balance
        self.withdrawal.delete()
        self.assertFalse(Balance.objects.filter(id=balance_record.id).exists())
