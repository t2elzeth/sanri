from rest_framework import generics

from authorization.models import User
from container.models import ContainerCar
from utils.mixins import DetailAPIViewMixin
from .filters import CarModelFilter
from .models import CarOrder
from .serializers import CarOrderSerializer, ParkingSerializer
from rest_framework.permissions import IsAuthenticated


class CarOrderAPIView(generics.ListCreateAPIView):
    queryset = CarOrder.objects.exclude(client=None)
    serializer_class = CarOrderSerializer
    filterset_class = CarModelFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type == User.USER_TYPE_CLIENT:
            self.queryset = self.queryset.filter(client=self.request.user)
        return super().get_queryset()


class CarOrderDetailAPIView(DetailAPIViewMixin):
    queryset = CarOrder.objects.all()
    serializer_class = CarOrderSerializer


class ParkingAPIView(generics.ListAPIView):
    queryset = CarOrder.objects.exclude(client=None)
    serializer_class = ParkingSerializer
    filterset_class = CarModelFilter

    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type == User.USER_TYPE_CLIENT:
            self.queryset = self.queryset.filter(client=self.request.user)

        car_ids = list(
            [
                el["car__id"]
                for el in ContainerCar.objects.all().values("car__id")
            ]
        )
        self.queryset = self.queryset.exclude(id__in=car_ids)
        return super().get_queryset()
