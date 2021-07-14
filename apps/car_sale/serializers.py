from rest_framework import serializers

from auction.models import Auction
from authorization.models import User
from car_order.models import CarOrder
from car_order.serializers import CarOrderSerializer
from .models import CarSale


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "fullName"]
        ref_name = "car_sale"


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ["id", "name"]


class CarSaleSerializer(serializers.ModelSerializer):
    ownerClient_id = serializers.PrimaryKeyRelatedField(
        source="ownerClient", write_only=True, queryset=User.objects.all()
    )
    auction_id = serializers.PrimaryKeyRelatedField(
        source="auction", write_only=True, queryset=Auction.objects.all()
    )
    ownerClient = ClientSerializer(read_only=True)
    auction = AuctionSerializer(read_only=True)

    carOrder_id = serializers.PrimaryKeyRelatedField(
        source="carOrder", write_only=True, queryset=CarOrder.objects.all()
    )
    carOrder = CarOrderSerializer(read_only=True)

    class Meta:
        model = CarSale
        fields = [
            "id",
            "ownerClient",
            "ownerClient_id",
            "auction",
            "auction_id",
            "carOrder",
            "carOrder_id",
            "price",
            "recycle",
            "auctionFees",
            "salesFees",
            "status",
            "total",
            "created_at",
        ]

    def validate(self, data):
        status = data.get("status", False)
        if self.instance and status:
            price = data.get("price", 0)
            recycle = data.get("recycle", 0)
            if price == 0 or recycle == 0:
                raise serializers.ValidationError(
                    "Recycle and price must be specified"
                )

        return super().validate(data)
