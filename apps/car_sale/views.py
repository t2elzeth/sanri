from rest_framework.viewsets import ModelViewSet

from .models import CarSale
from .serializers import CarSaleSerializer


class CarSaleViewSet(ModelViewSet):
    queryset = CarSale.objects.all()
    serializer_class = CarSaleSerializer
