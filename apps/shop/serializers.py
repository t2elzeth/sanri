from rest_framework import serializers

from .models import ShopCar, ShopImage, FuelEfficiency


class FuelEfficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelEfficiency
        fields = ['city', 'track']


class ShopImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopImage
        fields = ['image']


class ShopCarSerializer(serializers.ModelSerializer):
    fuel_efficiency = FuelEfficiencySerializer()
    images = ShopImageSerializer(many=True)

    class Meta:
        model = ShopCar
        fields = ['id', 'price', 'currency', 'hp', 'engine', 'fuel_efficiency', 'images']
