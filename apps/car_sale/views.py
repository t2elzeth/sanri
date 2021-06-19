from rest_framework import generics

from utils.mixins import DetailAPIViewMixin

from .models import CarSale
from .serializers import CarSaleSerializer


class CarSaleAPIView(generics.ListCreateAPIView):
    queryset = CarSale.objects.all()
    serializer_class = CarSaleSerializer


class CarSaleDetailAPIView(DetailAPIViewMixin):
    queryset = CarSale.objects.all()
    serializer_class = CarSaleSerializer
