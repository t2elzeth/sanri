from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from authorization.models import Balance
from .models import (
    Container,
    WheelRecycling,
    WheelSales,
    ContainerBalanceWithdrawal,
)


@receiver(pre_save, sender=Container)
def update_stock(instance: Container, **kwargs):
    instance.calculate_total()


@receiver(post_save, sender=Container)
def post_save_car_resale(instance: Container, created, **kwargs):
    if created:
        instance.save()

    if instance.status == Container.STATUS_SHIPPED:
        balance = Balance.objects.create(
            client=instance.client,
            sum_in_jpy=instance.totalAmount,
            rate=1,
            sum_in_usa=instance.totalAmount,
            payment_type=Balance.PAYMENT_TYPE_CASHLESS,
            sender_name="ContainerShipping",
            comment=f"For shipping container #{instance.id}",
            balance_action=Balance.BALANCE_ACTION_WITHDRAWAL,
        )
        ContainerBalanceWithdrawal.objects.create(
            balance=balance, container=instance
        )

    instance.container_withdrawal.calculate()


@receiver(post_save, sender=WheelRecycling)
def create_cound_and_sum(instance, created, **kwargs):
    if created:
        instance.container.save()


@receiver(post_save, sender=WheelSales)
def create_cound_and_sum(instance, created, **kwargs):
    if created:
        instance.container.save()
