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
from rest_framework.permissions import IsAuthenticated


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

    # def get_queryset(self):
    #     user_type = self.request.user.user_type
    #     if user_type == User.USER_TYPE_CLIENT:
    #         self.queryset = self.queryset.filter(id=self.request.user.id)
    #
    #     return super().get_queryset()


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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type == User.USER_TYPE_CLIENT:
            self.queryset = self.queryset.filter(client=self.request.user)
        return super().get_queryset()


class BalanceAPIView(DetailAPIViewMixin):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
