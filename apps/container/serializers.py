from rest_framework import serializers

from authorization.models import User
from car_order.models import CarOrder
from car_order.serializers import CarOrderSerializer
from .models import Container, CountAndSum, ContainerCar


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "fullName", "atWhatPrice"]
        ref_name = "container"


class CountAndSumSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountAndSum
        fields = ["count", "sum"]


class ContainerCarSerializer(serializers.ModelSerializer):
    car = CarOrderSerializer()

    class Meta:
        model = ContainerCar
        fields = ["container", "car"]
        ref_name = "container"


class ContainerSerializer(serializers.ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(
        source="client", write_only=True, queryset=User.objects.all()
    )
    client = ClientSerializer(read_only=True)
    wheelRecycling = CountAndSumSerializer(source="count_and_sum.first")
    wheelSales = CountAndSumSerializer(source="count_and_sum.last")
    car_ids = serializers.ListSerializer(
        child=serializers.IntegerField(), write_only=True
    )
    cars = ContainerCarSerializer(
        read_only=True, many=True, source="container_cars"
    )

    class Meta:
        model = Container
        fields = [
            "id",
            "client",
            "client_id",
            "name",
            "dateOfSending",
            "commission",
            "containerTransportation",
            "packagingMaterials",
            "transportation",
            "loading",
            "wheelRecycling",
            "wheelSales",
            "status",
            "totalAmount",
            "cars",
            "car_ids",
        ]
        extra_kwargs = {"totalAmount": {"read_only": True}}

    def create(self, validated_data: dict):
        # print("This is validated_data", validated_data)
        count_and_sum = validated_data.pop("count_and_sum", None)
        cars = validated_data.pop("car_ids", None)
        wheelRecycling = count_and_sum.pop("first", None)
        wheelSales = count_and_sum.pop("last", None)

        container = super().create(validated_data)
        if wheelRecycling is not None:
            data = {"container": container, **wheelRecycling}
            CountAndSum.objects.create(**data)

        if wheelSales is not None:
            data = {"container": container, **wheelSales}
            CountAndSum.objects.create(**data)

        for car in cars:
            container.container_cars.create(car=CarOrder.objects.get(id=car))

        return container
