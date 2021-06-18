from django.db import models


class CarResale(models.Model):
    ownerClientId = models.IntegerField()
    carOrderId = models.IntegerField()
    startingPrice = models.CharField(max_length=255)
    newClientId = models.IntegerField()
    salePrice = models.CharField(max_length=255)
    income = models.CharField(max_length=255)

    def __str__(self):
        return self.income
