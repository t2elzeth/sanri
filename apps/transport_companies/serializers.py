from rest_framework import serializers

from .models import TransportCompany

class TransportCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportCompany
        fields = ['id', 'name']

