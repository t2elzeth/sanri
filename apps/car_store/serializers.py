from rest_framework import serializers

from .models import CarStore, CarStoreImage


class CarStoreImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarStoreImage
        fields = ["id", "name"]


class CarStoreSerializer(serializers.ModelSerializer):
    images = CarStoreImageSerializer(many=True, read_only=True)
    imgs = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = CarStore
        fields = [
            "id",
            "brand",
            "model",
            "year",
            "milage",
            "body",
            "displacement",
            "complect",
            "condition",
            "price",
            "status",
            "imgs",
            "images",
        ]

    def create(self, validated_data: dict):
        images = validated_data.pop("imgs", None)

        car_store = super().create(validated_data)
        if images is not None:
            for image in images:
                car_store.images.create(name=image)

        return car_store
