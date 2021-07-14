from rest_framework import generics

from utils.mixins import DetailAPIViewMixin
from .filters import CarModelFilter
from .models import CarOrder
from .serializers import CarOrderSerializer


class CarOrderAPIView(generics.ListCreateAPIView):
    queryset = CarOrder.objects.exclude(client=None)
    serializer_class = CarOrderSerializer
    filterset_class = CarModelFilter


class CarOrderDetailAPIView(DetailAPIViewMixin):
    queryset = CarOrder.objects.all()
    serializer_class = CarOrderSerializer
