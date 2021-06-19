from rest_framework import generics

from .models import Container
from .serializers import ContainerSerializer


class ContainerAPIView(generics.ListCreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer


class ContainerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
