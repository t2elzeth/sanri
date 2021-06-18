from rest_framework import serializers

from .models import CarResale


class CarResaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarResale
        fields = [
            'ownerClientId',
            'carOrderId',
            'startingPrice',
            'newClientId',
            'salePrice',
            'income'
        ]
