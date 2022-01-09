from rest_framework import generics

from utils.mixins import DetailAPIViewMixin
from .models import TransportCompany
from .serializers import TransportCompanySerializer


class TransportCompanyAPIView(generics.ListCreateAPIView):
    """Создать новый или получить список аукционов"""

    queryset = TransportCompany.objects.all()
    serializer_class = TransportCompanySerializer


class TransportCompanyDetailAPIView(DetailAPIViewMixin):
    """Получить, изменить, удалить определенный аукцион"""

    queryset = TransportCompany.objects.all()
    serializer_class = TransportCompanySerializer
