from authorization.models import Balance
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import (
    ShopCar, ShopImage, FuelEfficiency, CarForApprove
)


@receiver(post_save, sender=CarForApprove)
def car_for_approve_post_save(instance: CarForApprove, created, **kwargs):
    if created:
        instance.shop_car.status = instance.shop_car.STATUS_FOR_APPROVE
        instance.shop_car.save()
