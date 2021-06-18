from rest_framework import serializers

from .models import CarSale


class CarSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarSale
        fields = [
            'ownerClientId',
            'auctionId',
            'carModel',
            'vinNumber',
            'price',
            'recycle',
            'auctionFees',
            'salesFees',
            'status',
            'total'
        ]
