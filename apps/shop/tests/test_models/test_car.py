from django.test import TestCase
from django.db import models
from shop.models import Car
from car_model.models import CarModel
from shop.models_factory import CarFactory


class TestCarFields(TestCase):
    def get_field(self, field_name: str) -> models.Field:
        return Car._meta.get_field(field_name)

    def test_model_field(self):
        field_name = "model"
        field = self.get_field(field_name)

        self.assertIsInstance(field, models.ForeignKey)
        self.assertEqual(field.remote_field.model, CarModel)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_year_field(self):
        field_name = "year"
        field = self.get_field(field_name)

        self.assertIsInstance(field, models.IntegerField)

    def test_volume_field(self):
        field_name = "volume"
        field = self.get_field(field_name)

        self.assertIsInstance(field, models.DecimalField)
        self.assertEqual(field.max_digits, 4)
        self.assertEqual(field.decimal_places, 2)

    def test_mileage_field(self):
        field_name = "mileage"
        field = self.get_field(field_name)

        self.assertIsInstance(field, models.DecimalField)
        self.assertEqual(field.max_digits, 20)
        self.assertEqual(field.decimal_places, 2)

    def test_condition_field(self):
        field_name = "condition"
        field = self.get_field(field_name)

        self.assertIsInstance(field, models.IntegerField)

    def test_price_field(self):
        field_name = "price"
        field = self.get_field(field_name)

        self.assertIsInstance(field, models.DecimalField)
        self.assertEqual(field.max_digits, 20)
        self.assertEqual(field.decimal_places, 2)

    def test_description_field(self):
        field_name = "description"
        field = self.get_field(field_name)

        self.assertIsInstance(field, models.TextField)

    def test_field_sold(self):
        field_name = "sold"
        field = self.get_field(field_name)

        self.assertIsInstance(field, models.BooleanField)
        self.assertEqual(field.default, False)


class TestCarStringRepresentation(TestCase):
    def setUp(self) -> None:
        self.instance: Car = CarFactory.create()

    def test_string_representation(self):
        string_representation = str(self.instance)
        expected = f"{self.instance.model.mark.name} | {self.instance.model.name} for {self.instance.price}"

        self.assertEqual(string_representation, expected)
