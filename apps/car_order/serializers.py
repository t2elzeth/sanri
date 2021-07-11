from rest_framework import serializers

from authorization.models import User
from car_model.models import CarModel, CarMark
from .models import CarOrder
from auction.models import Auction


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullName']
        ref_name = "car_order"


class CarMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMark
        fields = ['id', 'name']
        ref_name = "car_order"



class CarModelSerializer(serializers.ModelSerializer):
    mark = CarMarkSerializer()

    class Meta:
        model = CarModel
        fields = ['id', 'mark', 'name']
        ref_name = "car_order"


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'name']
        ref_name = "car_order"


class CarOrderSerializer(serializers.ModelSerializer):
    carModel_id = serializers.PrimaryKeyRelatedField(source='carModel',
                                                     write_only=True,
                                                     queryset=CarModel.objects.all())

    client_id = serializers.PrimaryKeyRelatedField(source="client",
                                                   write_only=True,
                                                   queryset=User.objects.all())

    auction_id = serializers.PrimaryKeyRelatedField(source='auction',
                                                    write_only=True,
                                                    queryset=Auction.objects.all())

    client = ClientSerializer(read_only=True)
    auction = AuctionSerializer(read_only=True)
    carModel = CarModelSerializer(read_only=True)

    def get_marka_name(self, obj):
        return f'{obj.carModel.mark.name} / {obj.carModel.name}'

    class Meta:
        model = CarOrder
        fields = [
            "id",
            "client",
            'client_id',
            'auction_id',
            'carModel',
            "auction",
            "lotNumber",
            "carModel_id",
            'documentsGiven',
            "vinNumber",
            "year",
            "price",
            "recycle",
            "auctionFees",
            "transport",
            "fob",
            "amount",
            "parking",
            "carNumber",
            "total",
            "total_FOB",
            "created_at",
        ]
