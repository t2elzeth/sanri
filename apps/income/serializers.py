from rest_framework import serializers

from .models import Income, IncomeType


class IncomeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeType
        fields = ["id", "name"]


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ["id", "type", "date", "amount", "comment"]
