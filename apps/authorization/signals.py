from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import User


@receiver(pre_save, sender=User)
def update_stock(instance: User, **kwargs):
    # AT_WHAT_PRICE_BY_FACT clients must have sizeFOB set to 0
    if instance.atWhatPrice == User.AT_WHAT_PRICE_BY_FACT:
        instance.sizeFOB = 0

    for car_order in instance.car_orders.all():
        if car_order.fob != instance.sizeFOB:
            car_order.save()


@receiver(post_save, sender=User)
def post_save_car_resale(instance: User, created, **kwargs):
    if created:
        instance.save()
