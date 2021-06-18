from rest_framework.viewsets import ModelViewSet

from .models import CarStore
from .serializers import CarStoreSerializer


class CarStoreViewSet(ModelViewSet):
    queryset = CarStore.objects.all()
    serializer_class = CarStoreSerializer
