from rest_framework import serializers

from .models import Income, IncomeType


class IncomeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeType
        fields = ["id", "name"]


class IncomeSerializer(serializers.ModelSerializer):
    type = IncomeTypeSerializer(read_only=True)

    type_id = serializers.PrimaryKeyRelatedField(source='type',
                                                 write_only=True,
                                                 queryset=IncomeType.objects.all())

    class Meta:
        model = Income
        fields = ["id", "type", 'type_id', "date", "amount", "comment"]
