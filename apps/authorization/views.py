from rest_framework import mixins, status, views, generics
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import TokenSerializer, UserSerializer


class RegisterAPIView(mixins.CreateModelMixin,
                      generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        response = self.create(request)
        response.status_code = status.HTTP_200_OK
        return response


class LoginAPIView(mixins.CreateModelMixin,
                      generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = TokenSerializer

    def post(self, request):
        response = self.create(request)
        response.status_code = status.HTTP_200_OK
        return response
