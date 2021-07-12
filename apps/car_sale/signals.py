from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import CarSale


@receiver(pre_save, sender=CarSale)
def update_stock(instance: CarSale, **kwargs):
    if not instance.status:
        instance.price = 0
        instance.recycle = 0

    instance.calculate_total()


@receiver(post_save, sender=CarSale)
def post_save_car_resale(instance, created, **kwargs):
    if created:
        instance.save()
