from rest_framework import generics

from utils.mixins import DetailAPIViewMixin
from .models import CarStore
from .serializers import CarStoreSerializer


class CarStoreAPIView(generics.ListCreateAPIView):
    queryset = CarStore.objects.all()
    serializer_class = CarStoreSerializer


class CarStoreDetailAPIView(DetailAPIViewMixin):
    queryset = CarStore.objects.all()
    serializer_class = CarStoreSerializer
