from django.db import models

from auction.models import Auction
from authorization.models import User
from car_order.models import CarOrder
from .formulas import calculate_total


class CarSale(models.Model):
    ownerClient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="car_sales_as_owner"
    )
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="car_sales"
    )
    carOrder = models.ForeignKey(
        CarOrder, on_delete=models.PROTECT, related_name="car_sales"
    )
    price = models.IntegerField(default=0)
    recycle = models.IntegerField(default=0)
    auctionFees = models.IntegerField()
    salesFees = models.IntegerField()
    status = models.BooleanField(default=False)
    total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        self.total = calculate_total(
            self.price, self.recycle, self.auctionFees, self.salesFees
        )

    def __str__(self):
        return self.price
