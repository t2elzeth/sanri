from rest_framework import serializers

from .models import Auction


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = [
            "id",
            "name",
            "parkingPrice1",
            "parkingPrice2",
            "parkingPrice3",
            "parkingPrice4",
        ]
