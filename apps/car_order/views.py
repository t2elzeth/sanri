from authorization.models import User
from container.models import ContainerCar
from django.core.cache import cache
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from utils.mixins import DetailAPIViewMixin

from .filters import CarModelFilter
from .models import CarOrder
from .serializers import CarOrderSerializer, ParkingSerializer


class CarOrderAPIView(generics.ListCreateAPIView):
    queryset = CarOrder.objects.exclude(client=None)
    serializer_class = CarOrderSerializer
    filterset_class = CarModelFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # print(cache.keys("*"))

        print(cache.keys("balance_list*"))

        user_type = self.request.user.user_type
        if user_type == User.USER_TYPE_CLIENT:
            self.queryset = self.queryset.filter(client=self.request.user)
        elif user_type in (
            User.USER_TYPE_SALES_MANAGER,
            User.USER_TYPE_YARD_MANAGER,
        ):
            managed_users = [
                managed_user.user
                for managed_user in self.request.user.managed_users_as_manager.all()
            ]
            self.queryset = self.queryset.filter(client__in=managed_users)
        return super().get_queryset()


class CarOrderDetailAPIView(DetailAPIViewMixin):
    queryset = CarOrder.objects.all()
    serializer_class = CarOrderSerializer


class ParkingAPIView(generics.ListAPIView):
    queryset = CarOrder.objects.exclude(client=None).exclude(is_sold=True)
    serializer_class = ParkingSerializer
    filterset_class = CarModelFilter

    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type == User.USER_TYPE_CLIENT:
            self.queryset = self.queryset.filter(client=self.request.user)
        elif user_type in (
            User.USER_TYPE_SALES_MANAGER,
            User.USER_TYPE_YARD_MANAGER,
        ):
            managed_users = [
                managed_user.user
                for managed_user in self.request.user.managed_users_as_manager.all()
            ]
            self.queryset = self.queryset.filter(client__in=managed_users)

        car_ids = list(
            [
                el["car__id"]
                for el in ContainerCar.objects.all().values("car__id")
            ]
        )
        self.queryset = self.queryset.exclude(id__in=car_ids)
        return super().get_queryset()
