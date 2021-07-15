from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Container, WheelRecycling, WheelSales
from authorization.models import Balance


@receiver(pre_save, sender=Container)
def update_stock(instance: Container, **kwargs):
    instance.calculate_total()


@receiver(post_save, sender=Container)
def post_save_car_resale(instance: Container, created, **kwargs):
    if created:
        instance.save()

    if instance.status == Container.STATUS_SHIPPED:
        Balance.objects.create(
            client=instance.client,
            sum_in_jpy=instance.totalAmount,
            rate=1,
            sum_in_usa=instance.totalAmount,
            payment_type=Balance.PAYMENT_TYPE_CASHLESS,
            sender_name="Container shipping",
            comment="Balance withdrawal from container shipping",
            balance_action=Balance.BALANCE_ACTION_WITHDRAWAL,
        )


@receiver(post_save, sender=WheelRecycling)
def create_cound_and_sum(instance, created, **kwargs):
    if created:
        instance.container.save()


@receiver(post_save, sender=WheelSales)
def create_cound_and_sum(instance, created, **kwargs):
    if created:
        instance.container.save()
