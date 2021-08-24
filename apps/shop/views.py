from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from utils.mixins import DetailAPIViewMixin
from .models import ShopCar, CarForApprove
from .serializers.read import ReadShopCarSerializer, ReadForApproveSerializer
from .serializers.write import WriteShopCarSerializer, WriteForApproveSerializer


class ShopCarAPIView(generics.ListCreateAPIView):
    queryset = ShopCar.objects.filter(status=ShopCar.STATUS_FOR_SELL)
    serializer_class = ReadShopCarSerializer


class ShopCarForApproveView(generics.ListCreateAPIView):
    queryset = CarForApprove.objects.all()
    serializer_class = ReadForApproveSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.serializer_class = WriteForApproveSerializer

        return super().get_serializer_class()


class ShopCarForApproveDetailAPIView(DetailAPIViewMixin):
    queryset = CarForApprove.objects.all()
    serializer_class = ReadForApproveSerializer


class ShopCarDetailAPIView(DetailAPIViewMixin):
    queryset = ShopCar.objects.all()
    serializer_class = ReadShopCarSerializer

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return WriteShopCarSerializer

        return super().get_serializer_class()
