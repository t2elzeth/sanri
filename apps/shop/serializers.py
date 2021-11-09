from rest_framework import serializers

from authorization.models import User
from car_model.serializers import CarModelSerializer
from shop.models import Car


class AddCarSerializer(serializers.Serializer):
    model_id = serializers.IntegerField()
    year = serializers.IntegerField()
    volume = serializers.DecimalField(max_digits=4, decimal_places=2)
    mileage = serializers.DecimalField(max_digits=20, decimal_places=2)
    condition = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=20, decimal_places=2)
    description = serializers.CharField()


class GetCarSerializer(serializers.ModelSerializer):
    model = CarModelSerializer()

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
        )


class AddBuyRequestSerializer(serializers.Serializer):
    from_client_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type=User.USER_TYPE_CLIENT)
    )
    car_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
