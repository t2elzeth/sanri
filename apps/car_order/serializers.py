from rest_framework import serializers

from .models import CarOrder


class CarOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarOrder
        fields = [
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
            "transportationCommission",
            "parking",
            "carNumber",
            "total",
            "total_FOB",
            'created_at'
        ]
