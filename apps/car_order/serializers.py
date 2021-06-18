from rest_framework import serializers

from .models import CarOrder


class CarOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarOrder
        fields = [
            "clientId",
            "auctionId",
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
            "transportationCommission",
            "parking",
            "carNumber",
            "total",
            "total_FOB",
        ]
