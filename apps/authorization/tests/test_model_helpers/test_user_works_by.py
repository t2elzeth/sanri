from authorization.models import User
from authorization.tests.factory import ClientFactory
from django.test import TestCase


class TestClientWorksBy(TestCase):
    def setUp(self) -> None:
        self.fact_client: User = ClientFactory.create(
            atWhatPrice=User.AT_WHAT_PRICE_BY_FACT
        )
        self.fob_client: User = ClientFactory.create(
            atWhatPrice=User.AT_WHAT_PRICE_BY_FOB
        )
        self.fob2_client: User = ClientFactory.create(
            atWhatPrice=User.AT_WHAT_PRICE_BY_FOB2
        )

    def test_get_works_by_fact(self):
        self.assertTrue(self.fact_client.works_by.by_fact)
        self.assertFalse(self.fob_client.works_by.by_fact)
        self.assertFalse(self.fob2_client.works_by.by_fact)

    def test_get_works_by_fob(self):
        self.assertFalse(self.fact_client.works_by.by_fob)
        self.assertTrue(self.fob_client.works_by.by_fob)
        self.assertFalse(self.fob2_client.works_by.by_fob)

    def test_get_works_by_fob2(self):
        self.assertFalse(self.fact_client.works_by.by_fob2)
        self.assertFalse(self.fob_client.works_by.by_fob2)
        self.assertTrue(self.fob2_client.works_by.by_fob2)

    def test_set_works_by_fact_true(self):
        self.fob_client.works_by.by_fact = True

        self.assertTrue(self.fob_client.works_by.by_fact)
        self.assertFalse(self.fob_client.works_by.by_fob)
        self.assertFalse(self.fob_client.works_by.by_fob2)

    def test_set_works_by_fob_true(self):
        self.fact_client.works_by.by_fob = True

        self.assertFalse(self.fact_client.works_by.by_fact)
        self.assertTrue(self.fact_client.works_by.by_fob)
        self.assertFalse(self.fact_client.works_by.by_fob2)

    def test_set_works_by_fob2_true(self):
        self.fact_client.works_by.by_fob2 = True

        self.assertFalse(self.fact_client.works_by.by_fact)
        self.assertFalse(self.fact_client.works_by.by_fob)
        self.assertTrue(self.fact_client.works_by.by_fob2)

    def test_set_works_by_false(self):
        self.fact_client.works_by.by_fact = False
        self.assertTrue(self.fact_client.works_by.by_fact)

        self.fob_client.works_by.by_fob = False
        self.assertTrue(self.fob_client.works_by.by_fact)

        self.fob2_client.works_by.by_fob2 = False
        self.assertTrue(self.fob2_client.works_by.by_fact)
