from .factory import CarMarkFactory, CarModelFactory

from django.test import TestCase


class TestCarModel(
    TestCase
):
    def test_create(self):
        mark = CarMarkFactory.create()
        model = CarModelFactory.create(mark=mark)
