from django.test import TestCase

from .factory import CarMarkFactory, CarModelFactory


class TestCarModel(TestCase):
    def test_create(self):
        mark = CarMarkFactory.create()
        model = CarModelFactory.create(mark=mark)
