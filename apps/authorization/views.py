from rest_framework import generics, mixins, status

from utils.mixins import DetailAPIViewMixin

from .models import Balance, User
from .serializers import (
    BalanceSerializer,
    ClientSerializer,
    EmployeeSerializer,
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


class ClientAPIView(DetailAPIViewMixin):
    queryset = User.objects.filter(user_type=User.USER_TYPE_CLIENT)
    serializer_class = ClientSerializer


class EmployeeAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(user_type=User.USER_TYPE_EMPLOYEE)
    serializer_class = EmployeeSerializer


class EmployeeDetailAPIView(DetailAPIViewMixin):
    queryset = User.objects.filter(user_type=User.USER_TYPE_EMPLOYEE)
    serializer_class = EmployeeSerializer


class BalanceListAPIView(generics.ListCreateAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer


class BalanceAPIView(DetailAPIViewMixin):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
