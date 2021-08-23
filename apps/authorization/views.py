from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated

from utils.mixins import DetailAPIViewMixin

from .filters import BalanceFilter
from .models import Balance, ManagedUser, User
from .serializers import (
    BalanceSerializer,
    ClientSerializer,
    ManagerSerializer,
    TokenSerializer,
    UserSerializer,
)


class RegisterAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        response = self.create(request)
        response.status_code = status.HTTP_200_OK
        return response


class LoginAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = TokenSerializer

    def post(self, request):
        response = self.create(request)
        response.status_code = status.HTTP_200_OK
        return response


class ClientListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(user_type=User.USER_TYPE_CLIENT)
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type in (
            User.USER_TYPE_SALES_MANAGER,
            User.USER_TYPE_YARD_MANAGER,
        ):
            self.queryset = [
                managed_user.user
                for managed_user in self.request.user.managed_users_as_manager.all()
            ]

        return super().get_queryset()


class ClientAPIView(DetailAPIViewMixin):
    queryset = User.objects.filter(user_type=User.USER_TYPE_CLIENT)
    serializer_class = ClientSerializer


class EmployeeAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(
        user_type=User.USER_TYPE_EMPLOYEE,
    )
    serializer_class = UserSerializer


class EmployeeDetailAPIView(DetailAPIViewMixin):
    queryset = User.objects.filter(user_type=User.USER_TYPE_EMPLOYEE)
    serializer_class = UserSerializer


class ManagerAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(
        user_type__in=(
            User.USER_TYPE_SALES_MANAGER,
            User.USER_TYPE_YARD_MANAGER,
        )
    )
    serializer_class = ManagerSerializer


class ManagerDetailAPIView(DetailAPIViewMixin):
    queryset = User.objects.filter(
        user_type__in=(
            User.USER_TYPE_SALES_MANAGER,
            User.USER_TYPE_YARD_MANAGER,
        )
    )
    serializer_class = ManagerSerializer


class BalanceListAPIView(generics.ListCreateAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BalanceFilter

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

        return super().get_queryset()


class BalanceAPIView(DetailAPIViewMixin):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
