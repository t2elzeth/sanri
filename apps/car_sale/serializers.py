from rest_framework import serializers

from .models import CarSale


class CarSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarSale
        fields = [
            "ownerClient",
            "auction",
            "carModel",
            "vinNumber",
            "price",
            "recycle",
            "auctionFees",
            "salesFees",
            "status",
            "total",
            'created_at'
        ]
