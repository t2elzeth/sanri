from rest_framework import mixins, status
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import TokenSerializer, UserSerializer


class AuthenticationViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=["post"], detail=False, serializer_class=UserSerializer)
    def register(self, request):
        response = self.create(request)
        response.status_code = status.HTTP_200_OK
        return response

    @action(methods=["post"], detail=False, serializer_class=TokenSerializer)
    def login(self, request):
        response = self.create(request)
        response.status_code = status.HTTP_200_OK
        return response

    # @action(
    #     methods=["post"], detail=False, permission_classes=[IsAuthenticated]
    # )
    # def logout(self, request):
    #     request.user.logout()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
