from rest_framework import generics

from utils.mixins import DetailAPIViewMixin

from .models import CarModel
from .serializers import CarModelSerializer
from .filters import CarModelFilter


class CarModelAPIView(generics.ListCreateAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    filterset_class = CarModelFilter


class CarModelDetailAPIView(DetailAPIViewMixin):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
