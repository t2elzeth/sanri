from rest_framework import serializers

from .models import CarOrder
from authorization.models import User


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname']


class CarOrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = CarOrder
        fields = [
            "id",
            "client",
            "auction",
            "lotNumber",
            "carModel",
            "vinNumber",
            "year",
            "price",
            "recycle",
            "auctionFees",
            "transport",
            "fob",
            "amount",
            # "transportationCommission",
            "parking",
            "carNumber",
            "total",
            "total_FOB",
            "created_at",
        ]
