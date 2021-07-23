from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import CarOrder, BalanceReplenishment


@receiver(pre_save, sender=CarOrder)
def update_stock(instance: CarOrder, **kwargs):
    instance.calculate_totals()


@receiver(post_save, sender=CarOrder)
def post_save_car_resale(instance: CarOrder, created, **kwargs):
    if created:
        BalanceReplenishment.objects.create(car_order=instance)
        instance.save()

    instance.replenishment.calculate_amount()
    instance.replenishment.save()
