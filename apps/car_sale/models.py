from django.db import models

from authorization.models import User
from auction.models import Auction
class CarSale(models.Model):
    ownerClient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car_sales_as_owner')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='car_sales')
    carModel = models.CharField(max_length=255, blank=True, null=True)
    vinNumber = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField()
    recycle = models.IntegerField()
    auctionFees = models.IntegerField()
    salesFees = models.IntegerField()
    status = models.BooleanField()
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.price
