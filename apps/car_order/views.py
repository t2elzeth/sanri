from rest_framework.viewsets import ModelViewSet

from .models import CarOrder
from .serializers import CarOrderSerializer


class CarOrderViewSet(ModelViewSet):
    queryset = CarOrder.objects.all()
    serializer_class = CarOrderSerializer
