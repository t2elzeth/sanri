from authorization.models import User
from car_order.models import CarOrder
from django.db import models


class CarResale(models.Model):
    ownerClient = models.ForeignKey(
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
    income = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.income}'
