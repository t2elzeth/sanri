from rest_framework import generics

from utils.mixins import DetailAPIViewMixin
from .models import CarModel
from .serializers import CarModelSerializer


class CarModelAPIView(generics.ListCreateAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class CarModelDetailAPIView(DetailAPIViewMixin):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
