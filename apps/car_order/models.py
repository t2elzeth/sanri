from django.contrib.auth import get_user_model
from django.db import models

from auction.models import Auction
from car_model.models import CarModel

User = get_user_model()


class CarOrder(models.Model):
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="car_orders"
    )
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="auctions"
    )
    lotNumber = models.CharField(max_length=255, blank=True, null=True)
    carModel = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_orders')
    vinNumber = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField()
    recycle = models.IntegerField()
    auctionFees = models.IntegerField()
    transport = models.IntegerField()
    fob = models.IntegerField()
    amount = models.IntegerField()
    # transportationCommission = models.IntegerField()
    parking = models.IntegerField()

    CAR_NUMBER_REMOVED = "removed"
    CAR_NUMBER_NOT_REMOVED = "not_removed"
    CAR_NUMBER_NOT_GIVEN = "not_given"
    CAR_NUMBER_STATUS_CHOICES = ((CAR_NUMBER_REMOVED, CAR_NUMBER_REMOVED),
                                 (CAR_NUMBER_NOT_REMOVED, CAR_NUMBER_NOT_REMOVED),
                                 (CAR_NUMBER_NOT_GIVEN, CAR_NUMBER_NOT_GIVEN))
    carNumber = models.CharField(max_length=255, choices=CAR_NUMBER_STATUS_CHOICES)
    total = models.IntegerField()
    total_FOB = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'CarOrder#{self.id} of {self.client.fullName}'
