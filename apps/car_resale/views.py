from rest_framework import generics

from utils.mixins import DetailAPIViewMixin

from .models import CarResale
from .serializers import CarResaleSerializer


class CarResaleAPIView(generics.ListCreateAPIView):
    queryset = CarResale.objects.all()
    serializer_class = CarResaleSerializer


class CarResaleDetailAPIView(DetailAPIViewMixin):
    queryset = CarResale.objects.all()
    serializer_class = CarResaleSerializer
