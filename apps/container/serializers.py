from rest_framework import serializers

from .models import Container, ContainerWheelRecycling, ContainerWheelSales


class ContainerWheelRecyclingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerWheelRecycling
        fields = ["count", "sum"]


class ContainerWheelSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerWheelSales
        fields = ["count", "sum"]


class ContainerSerializer(serializers.ModelSerializer):
    wheelRecycling = ContainerWheelRecyclingSerializer()
    wheelSales = ContainerWheelSalesSerializer()

    class Meta:
        model = Container
        fields = [
            "client",
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
        ]

    def create(self, validated_data: dict):
        wheelRecycling = validated_data.pop("wheelRecycling", None)
        wheelSales = validated_data.pop("wheelSales", None)

        container = super().create(validated_data)
        if wheelRecycling is not None:
            data = {
                'container': container,
                **wheelRecycling
            }
            ContainerWheelRecycling.objects.create(**data)

        if wheelSales is not None:
            data = {
                'container': container,
                **wheelSales
            }
            ContainerWheelSales.objects.create(**data)

        return container
