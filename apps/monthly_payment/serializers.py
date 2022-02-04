from rest_framework import serializers

from .models import MonthlyPayment, MonthlyPaymentType


class MonthlyPaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyPaymentType
        fields = ["id", "name"]


class WriteMonthlyPaymentSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="created_at")

    class Meta:
        model = MonthlyPayment
        fields = [
            "id",
            "type",
            "from_container",
            "date",
            "amount",
            "comment",
        ]


class ReadMonthlyPaymentSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="created_at")
    type = MonthlyPaymentTypeSerializer()

    class Meta:
        model = MonthlyPayment
        fields = ["id", "type", "from_container", "date", "amount", "comment"]
