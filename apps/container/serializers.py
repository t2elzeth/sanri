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
        wheelRecycling = validated_data.pop('wheelRecycling', None)
        if wheelRecycling is not None:
            serializer = ContainerWheelRecyclingSerializer(data=wheelRecycling)
            serializer.is_valid()
            wheelRecycling = serializer.save()
            validated_data.update({
                'wheelRecycling': wheelRecycling
            })

        wheelSales = validated_data.pop('wheelSales', None)
        if wheelSales is not None:
            serializer = ContainerWheelSalesSerializer(data=wheelSales)
            serializer.is_valid()
            wheelSales = serializer.save()
            validated_data.update({
                'wheelSales': wheelSales
            })

        return super().create(validated_data)
