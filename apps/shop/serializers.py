from authorization.serializers import ClientSerializer
from car_model.serializers import CarModelSerializer
from rest_framework import serializers
from shop.models import BuyRequest, Car, CarImage


class AddCarSerializer(serializers.Serializer):
    model_id = serializers.IntegerField()
    year = serializers.IntegerField()
    volume = serializers.DecimalField(max_digits=4, decimal_places=2)
    mileage = serializers.DecimalField(max_digits=20, decimal_places=2)
    condition = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=20, decimal_places=2)
    description = serializers.CharField()
    images = serializers.ListSerializer(
        child=serializers.FileField(), required=False, allow_null=True
    )


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ("image",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation["image"]


class GetCarSerializer(serializers.ModelSerializer):
    model = CarModelSerializer()
    images = CarImageSerializer(many=True)
    requests = serializers.IntegerField(source="buy_requests.count")

    class Meta:
        model = Car
        fields = (
            "id",
            "model",
            "year",
            "volume",
            "mileage",
            "condition",
            "price",
            "description",
            "images",
            "sold",
            "requests",
        )


class AddBuyRequestSerializer(serializers.Serializer):
    car_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())

    @property
    def validated_data(self):
        validated_data = super().validated_data
        car = validated_data.pop("car_id")
        validated_data.update({"car": car})
        return validated_data


class GetBuyRequestSerializer(serializers.ModelSerializer):
    car = GetCarSerializer()
    from_client = ClientSerializer()

    class Meta:
        model = BuyRequest
        fields = ("id", "car", "from_client", "status")


class ApproveBuyRequestSerializer(serializers.Serializer):
    request_id = serializers.PrimaryKeyRelatedField(
        queryset=BuyRequest.objects.filter(status=BuyRequest.STATUS_PENDING)
    )

    @property
    def validated_data(self):
        validated_data = super().validated_data
        request = validated_data.pop("request_id")
        validated_data.update({"request": request})

        return validated_data


class DeclineBuyRequestSerializer(serializers.Serializer):
    request_id = serializers.PrimaryKeyRelatedField(
        queryset=BuyRequest.objects.filter(status=BuyRequest.STATUS_PENDING)
    )

    @property
    def validated_data(self):
        validated_data = super().validated_data
        request = validated_data.pop("request_id")
        validated_data.update({"request": request})

        return validated_data
