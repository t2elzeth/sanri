from rest_framework.viewsets import ModelViewSet

from .models import CarResale
from .serializers import CarResaleSerializer


class CarResaleViewSet(ModelViewSet):
    queryset = CarResale.objects.all()
    serializer_class = CarResaleSerializer
