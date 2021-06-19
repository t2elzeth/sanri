from rest_framework import generics

from utils.mixins import DetailAPIViewMixin
from .models import Auction
from .serializers import AuctionSerializer


class AuctionAPIView(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer


class AuctionDetailAPIView(DetailAPIViewMixin):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
