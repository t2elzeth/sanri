from django.test import TestCase

from shop.models_factory import CarFactory
from shop.serializers import GetCarSerializer


class TestGetCarSerializer(TestCase):
    def setUp(self) -> None:
        self.car = CarFactory.create()
        self.serializer = GetCarSerializer(instance=self.car)
        self.serialized_data = self.serializer.data

    def test_keys(self):
        expected_keys = (
            "id",
            "model",
            "year",
            "volume",
            "mileage",
            "condition",
            "price",
            "description",
            "images",
        )
        received_keys = tuple(self.serialized_data.keys())

        self.assertEqual(received_keys, expected_keys)
