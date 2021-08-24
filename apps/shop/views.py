from rest_framework import generics

from utils.mixins import DetailAPIViewMixin
from .models import ShopCar
from .serializers.read import ReadShopCarSerializer
from .serializers.write import WriteShopCarSerializer


class ShopCarAPIView(generics.ListCreateAPIView):
    queryset = ShopCar.objects.all()
    serializer_class = ReadShopCarSerializer


class ShopCarDetailAPIView(DetailAPIViewMixin):
    queryset = ShopCar.objects.all()
    serializer_class = ReadShopCarSerializer

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return WriteShopCarSerializer

        return super().get_serializer_class()
