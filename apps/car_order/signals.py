from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import CarOrder


@receiver(pre_save, sender=CarOrder)
def update_stock(instance: CarOrder, **kwargs):
    instance.calculate_totals()


@receiver(post_save, sender=CarOrder)
def post_save_car_resale(instance, created, **kwargs):
    if created:
        instance.save()
