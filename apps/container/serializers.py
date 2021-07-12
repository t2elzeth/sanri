from rest_framework import serializers

from authorization.models import User
from .models import Container, CountAndSum


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "fullName"]
        ref_name = "car_order"


class CountAndSumSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountAndSum
        fields = ["id", "count", "sum"]


class ContainerSerializer(serializers.ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(
        source="client", write_only=True, queryset=User.objects.all()
    )
    client = ClientSerializer(read_only=True)
    wheelRecycling = CountAndSumSerializer(source="count_and_sum.first")
    wheelSales = CountAndSumSerializer(source="count_and_sum.last")

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
        ]

    def create(self, validated_data: dict):
        count_and_sum = validated_data.pop("count_and_sum", None)
        print(validated_data)
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
