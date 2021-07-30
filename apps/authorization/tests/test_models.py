from authorization.models import User
from django.test import TestCase


class TestClientCreate(TestCase):
    def setUp(self) -> None:
        self.client_by_fact = User.objects.create_user(
            password="123",
            fullName="My owner client",
            country="KG",
            email="ownerclient@gmail.com",
            phoneNumber="+996771221103",
            service=User.SERVICE_ENTIRE,
            atWhatPrice=User.AT_WHAT_PRICE_BY_FACT,
            username="client_by_fact",
        )

        self.client_by_fob = User.objects.create_user(
            password="123",
            fullName="My owner client",
            country="KG",
            email="ownerclient@gmail.com",
            phoneNumber="+996771221103",
            service=User.SERVICE_ENTIRE,
            atWhatPrice=User.AT_WHAT_PRICE_BY_FOB,
            username="client_by_fob",
        )

    def test_try_to_change_fob_for_by_fact_client(self):
        self.assertEqual(self.client_by_fact.sizeFOB, 0)

        self.client_by_fact.sizeFOB = 20000
        self.client_by_fact.save()
        self.assertEqual(self.client_by_fact.sizeFOB, 0)
