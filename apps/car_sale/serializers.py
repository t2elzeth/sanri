from rest_framework import serializers

from authorization.models import User
from .models import CarSale


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullName']
        ref_name = 'car_sale'


class CarSaleSerializer(serializers.ModelSerializer):
    ownerClient_id = serializers.PrimaryKeyRelatedField(source="ownerClient",
                                                        write_only=True,
                                                        queryset=User.objects.all())

    ownerClient = ClientSerializer(read_only=True)

    class Meta:
        model = CarSale
        fields = [
            "id",
            "ownerClient",
            "ownerClient_id",
            "auction",
            "carModel",
            "vinNumber",
            "price",
            "recycle",
            "auctionFees",
            "salesFees",
            "status",
            "total",
            "created_at",
        ]
