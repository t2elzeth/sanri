from django.db import models

from authorization.models import User
from car_order.models import CarOrder


class CarResale(models.Model):
    oldClient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="car_resales_as_owner"
    )
    carOrder = models.ForeignKey(
        CarOrder, on_delete=models.CASCADE, related_name="car_resales"
    )
    startingPrice = models.IntegerField()
    newClient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="car_resales_as_new_client",
    )
    salePrice = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.oldClient.username} -> {self.newClient.username} for {self.salePrice}"

    class Meta:
        ordering = ("id",)


class CarResaleOldClientReplenishment(models.Model):
    car_resale = models.OneToOneField(CarResale, on_delete=models.CASCADE, related_name='old_client_replenishment')
    balance = models.OneToOneField('authorization.Balance', on_delete=models.CASCADE,
                                   related_name='old_client_replenishment')

    def calculate(self):
        self.balance.sum_in_jpy = self.car_resale.carOrder.total
        self.balance.save()

    class Meta:
        ordering = ("id",)


class CarResaleNewClientWithdrawal(models.Model):
    car_resale = models.OneToOneField(CarResale, on_delete=models.CASCADE, related_name='new_client_withdrawal')
    balance = models.OneToOneField('authorization.Balance', on_delete=models.CASCADE,
                                   related_name='new_client_withdrawal')

    def calculate(self):
        self.balance.sum_in_jpy = self.car_resale.carOrder.total
        self.balance.save()

    class Meta:
        ordering = ("id",)
