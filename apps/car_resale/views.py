from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authorization.models import User
from utils.mixins import DetailAPIViewMixin
from .filters import CarResaleFilter
from .models import CarResale
from .serializers import CarResaleSerializer


class CarResaleAPIView(generics.ListCreateAPIView):
    queryset = CarResale.objects.all()
    serializer_class = CarResaleSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = CarResaleFilter

    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type == User.USER_TYPE_CLIENT:
            self.queryset = self.queryset.filter(oldClient=self.request.user)

        return super().get_queryset()


class CarResaleDetailAPIView(DetailAPIViewMixin):
    queryset = CarResale.objects.all()
    serializer_class = CarResaleSerializer
