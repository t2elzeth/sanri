from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import CarSale
from authorization.models import Balance


@receiver(pre_save, sender=CarSale)
def update_stock(instance: CarSale, **kwargs):
    if not instance.status:
        instance.price = 0
        instance.recycle = 0

    instance.calculate_total()


@receiver(post_save, sender=CarSale)
def post_save_car_resale(instance: CarSale, created, **kwargs):
    if created:
        instance.save()

    if instance.status:
        instance.carOrder.client = None
        instance.carOrder.save()

        Balance.objects.create(
            client=instance.ownerClient,
            sum_in_jpy=instance.total,
            sum_in_usa=instance.total,
            rate=1,
            payment_type=Balance.PAYMENT_TYPE_CASHLESS,
            balance_action=Balance.BALANCE_ACTION_REPLENISHMENT,
        )
