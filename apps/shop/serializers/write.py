import os
from urllib.parse import urlparse

from authorization.models import User
from car_model.models import CarModel
from car_model.serializers import CarModelSerializer
from django.db import models
from rest_framework import serializers
from shop.models import CarForApprove, ShopCar, ShopImage

from .common import FuelEfficiencySerializer, ShopImageSerializer


class WriteShopCarSerializer(serializers.ModelSerializer):
    fuel_efficiency = FuelEfficiencySerializer()
    images = serializers.ListSerializer(
        child=serializers.DictField(), write_only=True, required=False
    )
    image = serializers.ListSerializer(
        child=serializers.FileField(), write_only=True, required=False
    )

    model = CarModelSerializer(read_only=True)
    model_id = serializers.PrimaryKeyRelatedField(
        source="model", queryset=CarModel.objects.all()
    )

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
            "image",
        ]

    def create(self, validated_data: dict):
        new_images = validated_data.pop("image", None)
        fuel_efficiency = validated_data.pop("fuel_efficiency", None)

        car: ShopCar = super().create(validated_data)
        fe_serializer = FuelEfficiencySerializer(data=fuel_efficiency)
        fe_serializer.is_valid(raise_exception=False)
        fe_serializer.save(car=car)

        for img in new_images:
            car.images.create(image=img)

        return car

    def update(self, instance: ShopCar, validated_data: dict):
        new_images = validated_data.pop("image", [])
        old_images = validated_data.pop("images", [])
        fuel_efficiency = validated_data.pop(
            "fuel_efficiency", instance.fuel_efficiency
        )

        car: ShopCar = super().update(instance, validated_data)
        fe_serializer = FuelEfficiencySerializer(
            instance=instance.fuel_efficiency,
            data=fuel_efficiency,
            partial=True,
        )
        fe_serializer.is_valid()
        fe_serializer.save()

        car.images.all().delete()
        for img in new_images:
            car.images.create(image=img)

        for img in old_images:
            a = urlparse(img["image"])
            imagename = os.path.basename(a.path)  #
            ShopImage.objects.create(car=car, image=imagename)

        return car


class WriteForApproveSerializer(serializers.ModelSerializer):
    shop_car = serializers.PrimaryKeyRelatedField(
        queryset=ShopCar.objects.filter(status=ShopCar.STATUS_FOR_SELL)
    )

    class Meta:
        model = CarForApprove
        fields = ["shop_car"]

    def create(self, validated_data):
        validated_data.update({"client": self.context["request"].user})
        return super().create(validated_data)
