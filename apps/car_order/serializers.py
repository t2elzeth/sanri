from datetime import timedelta

from auction.models import Auction
from authorization.models import User
from car_model.models import CarMark, CarModel
from django.utils import timezone
from rest_framework import serializers
from transport_companies.models import TransportCompany

from .models import CarOrder


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "fullName"]
        ref_name = "car_order"


class CarMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMark
        fields = ["id", "name"]
        ref_name = "car_order"


class CarModelSerializer(serializers.ModelSerializer):
    mark = CarMarkSerializer()

    class Meta:
        model = CarModel
        fields = ["id", "mark", "name"]
        ref_name = "car_order"


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ["id", "name"]
        ref_name = "car_order"


class TransportCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportCompany
        fields = ["id", "name"]
        ref_name = "car_order"


class CarOrderSerializer(serializers.ModelSerializer):
    carModel_id = serializers.PrimaryKeyRelatedField(
        source="carModel", write_only=True, queryset=CarModel.objects.all()
    )

    client_id = serializers.PrimaryKeyRelatedField(
        source="client", write_only=True, queryset=User.objects.all()
    )

    auction_id = serializers.PrimaryKeyRelatedField(
        source="auction", write_only=True, queryset=Auction.objects.all()
    )

    transportCompany_id = serializers.PrimaryKeyRelatedField(
        source="transportCompany",
        write_only=True,
        queryset=TransportCompany.objects.all(),
    )

    client = ClientSerializer(read_only=True)
    auction = AuctionSerializer(read_only=True)
    carModel = CarModelSerializer(read_only=True)
    total = serializers.IntegerField(read_only=True)
    total_FOB = serializers.IntegerField(read_only=True)
    transportCompany = TransportCompanySerializer(read_only=True)

    # FOB property cannot be written, so its readonly
    fob = serializers.IntegerField(read_only=True)

    class Meta:
        model = CarOrder
        fields = [
            "id",
            "client",
            "client_id",
            "auction_id",
            "carModel",
            "auction",
            "lotNumber",
            "carModel_id",
            "documentsGiven",
            "vinNumber",
            "year",
            "price",
            "recycle",
            "auctionFees",
            "transport",
            "fob",
            "amount",
            "carNumber",
            "total",
            "total_FOB",
            "total_FOB2",
            "created_at",
            "transportCompany",
            "transportCompany_id",
            "analysis",
            "additional_expenses",
            "comment",
            "is_sold"
        ]


class ParkingSerializer(CarOrderSerializer):
    parked_until = serializers.SerializerMethodField(read_only=True)
    parked_for = serializers.SerializerMethodField(read_only=True)

    def get_parked_until(self, car):
        return car.created_at + timedelta(days=90)

    def get_parked_for(self, car):
        return (timezone.now().date() - car.created_at).days

    class Meta(CarOrderSerializer.Meta):
        fields = CarOrderSerializer.Meta.fields + [
            "parked_until",
            "parked_for",
        ]
