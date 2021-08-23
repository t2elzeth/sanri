from rest_framework import serializers

from .models import ShopCar, ShopImage, FuelEfficiency


class FuelEfficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelEfficiency
        fields = ["city", "track"]


class ShopImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopImage
        fields = ["image"]


class ShopCarSerializer(serializers.ModelSerializer):
    fuel_efficiency = FuelEfficiencySerializer()
    images = ShopImageSerializer(many=True, read_only=True)
    image = serializers.ListSerializer(child=serializers.FileField(), write_only=True)

    class Meta:
        model = ShopCar
        fields = [
            "id",
            "price",
            "currency",
            "hp",
            "engine",
            "fuel_efficiency",
            "images",
            "year",
            "millage",
            "condition",
            "body",
            "displacement",
            "complect",
            "status",
            "image"
        ]

    def create(self, validated_data: dict):
        images = validated_data.pop('image', None)

        return super().create(validated_data)
