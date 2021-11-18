from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from utils.mixins import DetailAPIViewMixin
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.core.cache import cache
from rest_framework.response import Response
from .filters import BalanceFilter
from .models import Balance, ManagedUser, User
from .serializers import (
    BalanceSerializer,
    ClientSerializer,
    ManagerSerializer,
    TokenSerializer,
    UserSerializer,
)

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from utils.cache import cache_action

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


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

    def retrieve(self, request, *args, **kwargs):
        print(cache.keys("*"))
        return super().retrieve(request, *args, **kwargs)


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

    @cache_action(key_prefix="balance_list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BalanceAPIView(DetailAPIViewMixin):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
