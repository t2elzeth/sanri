from django.db import models


class CarSale(models.Model):
    ownerClientId = models.IntegerField()
    auctionId = models.IntegerField()
    carModel = models.CharField(max_length=255)
    vinNumber = models.CharField(max_length=255)
    price = models.IntegerField()
    recycle = models.IntegerField()
    auctionFees = models.IntegerField()
    salesFees = models.IntegerField()
    status = models.BooleanField()
    total = models.IntegerField()

    def __str__(self):
        return self.price
