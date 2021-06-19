from rest_framework import generics

from .models import Container
from .serializers import ContainerSerializer


class ContainerAPIView(generics.CreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
