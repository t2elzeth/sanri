from authorization.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from utils.mixins import DetailAPIViewMixin

from .models import Container
from .serializers import ContainerSerializer


class ContainerAPIView(generics.ListCreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type == User.USER_TYPE_CLIENT:
            self.queryset = self.queryset.filter(client=self.request.user)
        elif user_type in (
            User.USER_TYPE_SALES_MANAGER,
            User.USER_TYPE_YARD_MANAGER,
            User.USER_TYPE_DILLER
        ):
            managed_users = [
                managed_user.user
                for managed_user in self.request.user.managed_users_as_manager.all()
            ]
            self.queryset = self.queryset.filter(client__in=managed_users)

        return super().get_queryset()


class ContainerDetailAPIView(DetailAPIViewMixin):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
