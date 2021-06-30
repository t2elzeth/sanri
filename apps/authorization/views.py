from rest_framework import generics, mixins, status

from utils.mixins import DetailAPIViewMixin

from .models import User
from .serializers import (ClientSerializer, EmployeeSerializer,
                          TokenSerializer, UserSerializer)


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
    queryset = User.objects.all()
    serializer_class = ClientSerializer


class ClientAPIView(DetailAPIViewMixin):
    queryset = User.objects.all()
    serializer_class = ClientSerializer


class EmployeeAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetailAPIView(DetailAPIViewMixin):
    queryset = User.objects.all()
    serializer_class = EmployeeSerializer
