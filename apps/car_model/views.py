from rest_framework import generics

from utils.mixins import DetailAPIViewMixin
from .filters import CarModelFilter
from .models import CarMark, CarModel
from .serializers import CarMarkSerializer, CarModelSerializer


class CarModelAPIView(generics.ListCreateAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    filterset_class = CarModelFilter


class CarModelDetailAPIView(DetailAPIViewMixin):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class CarMarkListAPIView(generics.ListAPIView):
    queryset = CarMark.objects.all()
    serializer_class = CarMarkSerializer
