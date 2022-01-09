from rest_framework import serializers

from authorization.models import User
from car_order.models import CarOrder
from car_order.serializers import CarOrderSerializer
from .models import Container, ContainerCar, WheelRecycling, WheelSales


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "fullName", "atWhatPrice"]
        ref_name = "container"


class WheelRecyclingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WheelRecycling
        fields = ["count", "sum"]


class WheelSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WheelSales
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
    wheelRecycling = WheelRecyclingSerializer(source="wheel_recycling")
    wheelSales = WheelSalesSerializer(source="wheel_sales")
    car_ids = serializers.ListSerializer(
        child=serializers.IntegerField(), write_only=True
    )
    cars = ContainerCarSerializer(
        read_only=True, many=True, source="container_cars"
    )

    # Annotated fields
    total = serializers.IntegerField(read_only=True)
    auctionFeesTotal = serializers.IntegerField(read_only=True)
    transportationTotal = serializers.IntegerField(read_only=True)
    price10Total = serializers.IntegerField(read_only=True)
    recycleTotal = serializers.IntegerField(read_only=True)
    amountTotal = serializers.IntegerField(read_only=True)
    fobTotal = serializers.IntegerField(read_only=True)
    income = serializers.IntegerField(read_only=True)
    overall = serializers.IntegerField(read_only=True)

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
            "total",
            "auctionFeesTotal",
            "transportationTotal",
            "price10Total",
            "recycleTotal",
            "amountTotal",
            "fobTotal",
            "income",
            "overall",
        ]
        extra_kwargs = {"totalAmount": {"read_only": True}}

    def create(self, validated_data: dict):

        cars = validated_data.pop("car_ids", None)
        wheelRecycling = validated_data.pop("wheel_recycling", None)
        wheelSales = validated_data.pop("wheel_sales", None)

        container = super().create(validated_data)
        if wheelRecycling is not None:
            data = {"container": container, **wheelRecycling}
            WheelRecycling.objects.create(**data)

        if wheelSales is not None:
            data = {"container": container, **wheelSales}
            WheelSales.objects.create(**data)

        for car in cars:
            container.container_cars.create(car=CarOrder.objects.get(id=car))

        return container

    def update(self, instance, validated_data):
        wheelRecycling = instance.wheel_recycling
        wheelSales = instance.wheel_sales

        wheelRecycle_data = validated_data.pop("wheel_recycling", {})
        wheelSales_data = validated_data.pop("wheel_sales", {})
        cars = validated_data.pop("car_ids", [])

        wheelRecycling.count = wheelRecycle_data.get(
            "count", wheelRecycling.count
        )
        wheelRecycling.sum = wheelRecycle_data.get("sum", wheelRecycling.sum)
        wheelRecycling.save()

        wheelSales.count = wheelSales_data.get("count", wheelSales.count)
        wheelSales.sum = wheelSales_data.get("sum", wheelSales.sum)
        wheelSales.save()

        instance.container_cars.all().delete()
        for car in cars:
            instance.container_cars.create(car=CarOrder.objects.get(id=car))

        return super().update(instance, validated_data)
