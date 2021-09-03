from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from utils.mixins import DetailAPIViewMixin

from .models import CarForApprove, ShopCar
from .serializers.read import ReadForApproveSerializer, ReadShopCarSerializer
from .serializers.write import (
    WriteForApproveSerializer,
    WriteShopCarSerializer,
)


class ShopCarAPIView(generics.ListCreateAPIView):
    queryset = ShopCar.objects.filter(status=ShopCar.STATUS_FOR_SELL)
    serializer_class = ReadShopCarSerializer


class ShopCarForApproveView(generics.ListCreateAPIView):
    queryset = CarForApprove.objects.all()
    serializer_class = ReadForApproveSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            self.serializer_class = WriteForApproveSerializer

        return super().get_serializer_class()


class ShopCarForApproveDetailAPIView(DetailAPIViewMixin):
    queryset = CarForApprove.objects.all()
    serializer_class = ReadForApproveSerializer


class ShopCarDetailAPIView(DetailAPIViewMixin):
    queryset = ShopCar.objects.all()
    serializer_class = ReadShopCarSerializer

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return WriteShopCarSerializer

        return super().get_serializer_class()
