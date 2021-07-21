from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authorization.models import User
from utils.mixins import DetailAPIViewMixin
from .models import CarSale
from .serializers import CarSaleSerializer


class CarSaleAPIView(generics.ListCreateAPIView):
    queryset = CarSale.objects.all()
    serializer_class = CarSaleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type == User.USER_TYPE_CLIENT:
            self.queryset = self.queryset.filter(ownerClient=self.request.user)

        return super().get_queryset()


class CarSaleDetailAPIView(DetailAPIViewMixin):
    queryset = CarSale.objects.all()
    serializer_class = CarSaleSerializer
