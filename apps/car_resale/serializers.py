from rest_framework import serializers

from authorization.models import User
from car_model.models import CarModel, CarMark
from car_order.models import CarOrder
from .models import CarResale


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullName']
        ref_name = 'car_resale'


class CarMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMark
        fields = ['id', 'name']
        ref_name = "car_resale"


class CarModelSerializer(serializers.ModelSerializer):
    mark = CarMarkSerializer()

    class Meta:
        model = CarModel
        fields = ['id', 'mark', 'name']
        ref_name = "car_resale"


class CarOrderSerializer(serializers.ModelSerializer):
    carModel = CarModelSerializer()

    class Meta:
        model = CarOrder
        fields = ['id', 'carModel']
        ref_name = "car_resale"


class CarResaleSerializer(serializers.ModelSerializer):
    ownerClient_id = serializers.PrimaryKeyRelatedField(source='ownerClient',
                                                        write_only=True,
                                                        queryset=User.objects.all())
    newClient_id = serializers.PrimaryKeyRelatedField(source='newClient',
                                                        write_only=True,
                                                        queryset=User.objects.all())
    carOrder_id = serializers.PrimaryKeyRelatedField(source="carOrder",
                                                     write_only=True,
                                                     queryset=CarOrder.objects.all())

    carOrder = CarOrderSerializer(read_only=True)
    ownerClient = ClientSerializer(read_only=True)
    newClient = ClientSerializer(read_only=True)

    class Meta:
        model = CarResale
        fields = [
            "id",
            "ownerClient",
            "ownerClient_id",
            "carOrder",
            "carOrder_id",
            "startingPrice",
            "newClient",
            "newClient_id",
            "salePrice",
            "income",
            "created_at",
        ]
