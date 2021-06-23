from rest_framework import serializers

from .models import CarResale


class CarResaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarResale
        fields = [
            "id",
            "ownerClient",
            "carOrder",
            "startingPrice",
            "newClient",
            "salePrice",
            "income",
            "created_at",
        ]
