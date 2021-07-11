from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import CarResale


@receiver(pre_save, sender=CarResale)
def update_stock(instance: CarResale, **kwargs):
    instance.income = instance.salePrice - instance.startingPrice


@receiver(post_save, sender=CarResale)
def post_save_car_resale(instance, created, **kwargs):
    if created:
        instance.save()
