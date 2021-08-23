from rest_framework import generics

from utils.mixins import DetailAPIViewMixin
from .models import ShopCar
from .serializers import ShopCarSerializer


class ShopCarAPIView(generics.ListCreateAPIView):
    queryset = ShopCar.objects.all()
    serializer_class = ShopCarSerializer


class ShopCarDetailAPIView(DetailAPIViewMixin):
    queryset = ShopCar.objects.all()
    serializer_class = ShopCarSerializer
