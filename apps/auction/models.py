from django.db import models


class Auction(models.Model):
    name = models.CharField(max_length=255)
    parkingPrice1 = models.CharField(max_length=255)
    parkingPrice2 = models.CharField(max_length=255)
    parkingPrice3 = models.CharField(max_length=255)
    parkingPrice4 = models.CharField(max_length=255)

    def __str__(self):
        return self.name
