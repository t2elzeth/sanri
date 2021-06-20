from django.db import models


class Auction(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    parkingPrice1 = models.CharField(max_length=255, blank=True, null=True)
    parkingPrice2 = models.CharField(max_length=255, blank=True, null=True)
    parkingPrice3 = models.CharField(max_length=255, blank=True, null=True)
    parkingPrice4 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
