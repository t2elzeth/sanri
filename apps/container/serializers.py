from rest_framework import serializers

from .models import Container, CountAndSum


class CountAndSumSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountAndSum
        fields = ["id", "count", "sum"]


class ContainerSerializer(serializers.ModelSerializer):
    wheelRecycling = CountAndSumSerializer(source="count_and_sum.first")
    wheelSales = CountAndSumSerializer(source="count_and_sum.last")

    class Meta:
        model = Container
        fields = [
            "id",
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
        count_and_sum = validated_data.pop("count_and_sum", None) 
        wheelRecycling = count_and_sum.pop("wheelRecycling", None)
        wheelSales = count_and_sum.pop("wheelSales", None)

        container = super().create(validated_data)
        if wheelRecycling is not None:
            data = {"container": container, **wheelRecycling}
            CountAndSum.objects.create(**data)

        if wheelSales is not None:
            data = {"container": container, **wheelSales}
            CountAndSum.objects.create(**data)

        return container
