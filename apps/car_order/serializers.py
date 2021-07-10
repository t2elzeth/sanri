from rest_framework import serializers

from .models import CarOrder
from authorization.models import User


class CarOrderSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.fullName', read_only=True)

    class Meta:
        model = CarOrder
        fields = [
            "id",
            "client",
            'client_name',
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
