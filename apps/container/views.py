from rest_framework import generics

from utils.mixins import DetailAPIViewMixin
from authorization.models import User

from .models import Container
from .serializers import ContainerSerializer
from rest_framework.permissions import IsAuthenticated


class ContainerAPIView(generics.ListCreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type == User.USER_TYPE_CLIENT:
            self.queryset = self.queryset.filter(client=self.request.user)

        return super().get_queryset()


class ContainerDetailAPIView(DetailAPIViewMixin):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
