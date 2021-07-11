from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import CarResale


@receiver(pre_save, sender=CarResale)
def update_stock(instance: CarResale, **kwargs):
    instance.income = instance.salePrice - instance.startingPrice


@receiver(post_save, sender=CarResale)
def post_save_car_resale(instance: CarResale, created, **kwargs):
    if created:
        car_order = instance.carOrder
        car_order.price = instance.salePrice
        car_order.client = instance.newClient
        if instance.newClient.atWhatPrice == instance.newClient.AT_WHAT_PRICE_BY_FOB:
            car_order.fob = instance.newClient.sizeFOB
        else:
            car_order.fob = 0
        car_order.save()
