import os
from urllib.parse import urlparse

from car_model.models import CarModel
from car_model.serializers import CarModelSerializer
from rest_framework import serializers
from rest_framework.generics import UpdateAPIView
from shop.models import FuelEfficiency, ShopCar, ShopImage


class FuelEfficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelEfficiency
        fields = ["city", "track"]


class ShopImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopImage
        fields = ["id", "image"]
