from django.db import models


class CarOrder(models.Model):
    clientId = models.IntegerField()
    auctionId = models.IntegerField()
    lotNumber = models.CharField(max_length=255)
    carModel = models.CharField(max_length=255)
    vinNumber = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    price = models.IntegerField()
    recycle = models.IntegerField()
    auctionFees = models.IntegerField()
    transport = models.IntegerField()
    fob = models.IntegerField()
    amount = models.IntegerField()
    transportationCommission = models.IntegerField()
    parking = models.IntegerField()
    carNumber = models.BooleanField()
    total = models.IntegerField()
    total_FOB = models.IntegerField()

    def __str__(self):
        return self.carModel
