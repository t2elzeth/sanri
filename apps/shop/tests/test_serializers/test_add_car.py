# from django.test import TestCase
#
# from car_model.tests.factory import CarModelFactory
# from shop.serializers import AddCarSerializer
#
#
# class TestAddCarSerializerValidatedData(TestCase):
#     def setUp(self) -> None:
#         self.model = CarModelFactory.create()
#         self.data = {
#             "model_id": self.model.id,
#             "year": 2003,
#             "volume": 4.5,
#             "mileage": 195_000.45,
#             "condition": 5,
#             "price": 25000,
#             "description": "The best car you have ever seen"
#         }
#         serializer = AddCarSerializer(data=self.data)
#         serializer.is_valid()
#         self.validated_data = serializer.validated_data
#
#     def test_validated_data(self):
#         expected_data = {
#             "model_id": self.model,
#             "year": 2003,
#             "volume": 4.5,
#             "mileage": 195_000.45,
#             "condition": 5,
#             "price": 25000,
#             "description": "The best car you have ever seen"
#         }
#
#         self.assertEqual(self.validated_data, expected_data)
