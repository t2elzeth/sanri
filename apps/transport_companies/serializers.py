from car_order.serializers import CarOrderSerializer
from rest_framework import serializers

from .models import TransportCompany


class TransportCompanySerializer(serializers.ModelSerializer):
    cars = CarOrderSerializer(source="car_orders", many=True, read_only=True)

    class Meta:
        model = TransportCompany
        fields = ["id", "name", "cars"]
