from rest_framework import generics

from utils.mixins import DetailAPIViewMixin

from .models import CarOrder
from .serializers import CarOrderSerializer


class CarOrderAPIView(generics.ListCreateAPIView):
    queryset = CarOrder.objects.all()
    serializer_class = CarOrderSerializer


class CarOrderDetailAPIView(DetailAPIViewMixin):
    queryset = CarOrder.objects.all()
    serializer_class = CarOrderSerializer
