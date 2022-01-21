from authorization.models import User
from django.db import models
from django.test import TestCase
from shop.models import BuyRequest, Car


class TestBuyRequestFields(TestCase):
    def get_field(self, field_name: str) -> models.Field:
        return BuyRequest._meta.get_field(field_name)

    def test_field_from_client(self):
        field_name = "from_client"
        field = self.get_field(field_name)

        self.assertIsInstance(field, models.ForeignKey)
        self.assertEqual(field.remote_field.model, User)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_field_car(self):
        field_name = "car"
        field = self.get_field(field_name)

        self.assertIsInstance(field, models.ForeignKey)
        self.assertEqual(field.remote_field.model, Car)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_field_approved(self):
        field_name = "approved"
        field = self.get_field(field_name)

        self.assertIsInstance(field, models.BooleanField)
        self.assertEqual(field.default, False)
