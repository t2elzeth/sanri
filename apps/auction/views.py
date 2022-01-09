from rest_framework import generics

from utils.mixins import DetailAPIViewMixin
from .models import Auction
from .serializers import AuctionSerializer


class AuctionAPIView(generics.ListCreateAPIView):
    """Создать новый или получить список аукционов"""

    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer


class AuctionDetailAPIView(DetailAPIViewMixin):
    """Получить, изменить, удалить определенный аукцион"""

    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
