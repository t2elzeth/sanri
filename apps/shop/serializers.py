from rest_framework import serializers

from .models import ShopCar, ShopImage, FuelEfficiency
from car_model.models import CarModel
from car_model.serializers import CarModelSerializer


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

    model = CarModelSerializer(read_only=True)
    model_id = serializers.PrimaryKeyRelatedField(source="model", queryset=CarModel.objects.all())

    class Meta:
        model = ShopCar
        fields = [
            "id",
            "price",
            "currency",
            "hp",
            "engine",
            "model",
            "model_id",
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
        fuel_efficiency = validated_data.pop('fuel_efficiency', None)

        car: ShopCar = super().create(validated_data)
        fe_serializer = FuelEfficiencySerializer(data=fuel_efficiency)
        fe_serializer.is_valid(raise_exception=False)
        fe_serializer.save(car=car)

        return car
