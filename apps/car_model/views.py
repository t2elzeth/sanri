from rest_framework.viewsets import ModelViewSet

from .models import CarModel
from .serializers import CarModelSerializer


class CarModelViewSet(ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
