from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import CarResale


@receiver(pre_save, sender=CarResale)
def update_stock(instance: CarResale, **kwargs):
    instance.income = instance.salePrice - instance.startingPrice
