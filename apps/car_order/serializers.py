from rest_framework import serializers

from authorization.models import User
from car_model.models import CarModel, CarMark
from .models import CarOrder
from auction.models import Auction


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullName']


class CarOrderMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMark
        fields = ['id', 'name']


class CarOrderModelSerializer(serializers.ModelSerializer):
    mark = CarOrderMarkSerializer()

    class Meta:
        model = CarModel
        fields = ['id', 'mark', 'name']


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'name']


class CarOrderSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.fullName', read_only=True)
    marka_name = serializers.SerializerMethodField(read_only=True)
    auction_name = serializers.CharField(source="auction.name", read_only=True)
    carModelDetail = CarOrderModelSerializer(source='carModel', read_only=True)
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
    carModel = CarOrderModelSerializer(read_only=True)

    def get_marka_name(self, obj):
        return f'{obj.carModel.mark.name} / {obj.carModel.name}'

    class Meta:
        model = CarOrder
        fields = [
            "id",
            "client",
            'client_id',
            'client_name',
            'auction_id',
            'carModel',
            'marka_name',
            'auction_name',
            "auction",
            "lotNumber",
            "carModel_id",
            "carModelDetail",
            'documentsGiven',
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
