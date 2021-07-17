from rest_framework import generics

from utils.mixins import DetailAPIViewMixin
from .filters import CarModelFilter
from .models import CarOrder
from .serializers import CarOrderSerializer, ParkingSerializer
from container.models import ContainerCar


class CarOrderAPIView(generics.ListCreateAPIView):
    queryset = CarOrder.objects.exclude(client=None)
    serializer_class = CarOrderSerializer
    filterset_class = CarModelFilter


class CarOrderDetailAPIView(DetailAPIViewMixin):
    queryset = CarOrder.objects.all()
    serializer_class = CarOrderSerializer


class ParkingAPIView(generics.ListAPIView):
    serializer_class = ParkingSerializer

    def get_queryset(self):
        car_ids = list([el['car__id'] for el in ContainerCar.objects.all().values('car__id')])
        queryset = CarOrder.objects.exclude(id__in=car_ids).exclude(client=None)
        print(queryset)
        return queryset
