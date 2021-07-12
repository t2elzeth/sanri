from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import User


@receiver(pre_save, sender=User)
def update_stock(instance: User, **kwargs):
    if instance.atWhatPrice == User.AT_WHAT_PRICE_BY_FACT:
        instance.sizeFOB = 0


@receiver(post_save, sender=User)
def post_save_car_resale(instance: User, created, **kwargs):
    if created:
        instance.save()