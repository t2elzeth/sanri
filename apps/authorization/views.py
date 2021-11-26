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
from rest_framework import views
from rest_framework.pagination import PageNumberPagination

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from utils.cache import cache_action
from django.db.models import Q

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
        return super().retrieve(request, *args, **kwargs)


class GetMeAPIView(views.APIView):
    permission_classes = (
        IsAuthenticated,
    )

    @cache_action("get-me")
    def get(self, request):
        user = self.request.user
        serializer = ClientSerializer(instance=user)
        return Response(serializer.data)


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


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class BalanceFilters:
    IS_REPLENISHMENT = Q(balance_action=Balance.BALANCE_ACTION_REPLENISHMENT)
    IS_WITHDRAWAL = Q(balance_action=Balance.BALANCE_ACTION_WITHDRAWAL)
    IS_CASHLESS = Q(payment_type=Balance.PAYMENT_TYPE_CASHLESS)
    IS_CASH = Q(payment_type=Balance.PAYMENT_TYPE_CASH)
    IS_FOR_RESALE = Q(sender_name__icontains="CarResale".lower())
    IS_SOLD = Q(comment__icontains="продали".lower())
    IS_FOR_ORDER = Q(sender_name__icontains="CarOrder".lower())


class BalanceListAPIView(generics.ListCreateAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BalanceFilter
    pagination_class = LargeResultsSetPagination

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

        group_name = self.request.query_params.get("group_name")
        if group_name == "clr":
            self.queryset = self.queryset.filter(
                BalanceFilters.IS_REPLENISHMENT,
                BalanceFilters.IS_CASHLESS
            ).exclude(
                BalanceFilters.IS_FOR_RESALE,
                BalanceFilters.IS_SOLD
            )
        elif group_name == "cr":
            self.queryset = self.queryset.filter(
                (BalanceFilters.IS_REPLENISHMENT & BalanceFilters.IS_CASH) |
                (BalanceFilters.IS_REPLENISHMENT & BalanceFilters.IS_FOR_RESALE) |
                BalanceFilters.IS_SOLD
            )
        elif group_name == "clw":
            self.queryset = self.queryset.filter(
                BalanceFilters.IS_WITHDRAWAL,
                BalanceFilters.IS_CASHLESS
            ).exclude(
                BalanceFilters.IS_FOR_ORDER,
                BalanceFilters.IS_FOR_RESALE
            )

        elif group_name == "cw":
            self.queryset = self.queryset.filter(
                BalanceFilters.IS_WITHDRAWAL,
                BalanceFilters.IS_CASH
            )
        elif group_name == "orders":
            self.queryset = (self.queryset
                             .filter(BalanceFilters.IS_WITHDRAWAL)
                             .filter(BalanceFilters.IS_FOR_ORDER | BalanceFilters.IS_FOR_RESALE))

        return super().get_queryset()

    # @cache_action(key_prefix="balances")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BalanceAPIView(DetailAPIViewMixin):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
