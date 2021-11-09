from rest_framework import serializers

from .models import CarMark, CarModel


class CarMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMark
        fields = ["id", "name"]


class CarModelSerializer(serializers.ModelSerializer):
    mark_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=CarMark.objects.all()
    )
    mark = CarMarkSerializer(read_only=True)

    class Meta:
        model = CarModel
        fields = ["id", "mark", "name", "mark_id"]
