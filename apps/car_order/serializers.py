from rest_framework import serializers

from car_model.models import CarModel
from .models import CarOrder


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'mark', 'name']
        depth = 2


class CarOrderSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.fullName', read_only=True)
    marka_name = serializers.SerializerMethodField(read_only=True)
    auction_name = serializers.CharField(source="auction.name", read_only=True)
    carModelDetail = CarModelSerializer(source="carModel", read_only=True)

    def get_marka_name(self, obj):
        return f'{obj.carModel.mark.name} / {obj.carModel.name}'

    class Meta:
        model = CarOrder
        fields = [
            "id",
            "client",
            'client_name',
            'marka_name',
            'auction_name',
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
