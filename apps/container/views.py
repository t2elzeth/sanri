from rest_framework import generics

from utils.mixins import DetailAPIViewMixin
from .models import Container
from .serializers import ContainerSerializer


class ContainerAPIView(generics.ListCreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer


class ContainerDetailAPIView(DetailAPIViewMixin):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
