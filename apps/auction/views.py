from rest_framework.viewsets import ModelViewSet

from .models import Auction
from .serializers import AuctionSerializer


class AuctionViewSet(ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
