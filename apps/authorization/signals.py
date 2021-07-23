from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import User, Balance


@receiver(pre_save, sender=User)
def update_stock(instance: User, **kwargs):
    if instance.atWhatPrice == User.AT_WHAT_PRICE_BY_FACT:
        instance.sizeFOB = 0


@receiver(post_save, sender=User)
def post_save_car_resale(instance: User, created, **kwargs):
    if created:
        instance.save()


@receiver(pre_save, sender=Balance)
def pre_save_balance(instance: Balance, **kwargs):

    # Теперь можно будет менять только sum_in_jpy, а sum_in_usa поменяется само, если rate === 1
    if instance.sum_in_jpy != instance.sum_in_usa and instance.rate == 1:
        instance.sum_in_usa = instance.sum_in_jpy
