from rest_framework import serializers

from .models import MonthlyPayment, MonthlyPaymentType


class MonthlyPaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyPaymentType
        fields = ["id", "name"]


class MonthlyPaymentSerializer(serializers.ModelSerializer):
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
