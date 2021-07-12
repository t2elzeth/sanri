from rest_framework import serializers

from .models import CarModel, CarMark


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ["id", "mark", "name"]


class CarMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMark
        fields = ["id", "name"]
