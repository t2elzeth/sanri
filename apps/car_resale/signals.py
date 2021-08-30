from authorization.models import Balance
from car_order.models import CarOrder
from car_sale.models import CarSale
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from income.models import Income, IncomeType

from .models import (
    CarResale,
    CarResaleNewClientWithdrawal,
    CarResaleOldClientReplenishment,
)


@receiver(pre_save, sender=CarResale)
def update_stock(instance: CarResale, **kwargs):
    instance.income = instance.salePrice - instance.startingPrice


@receiver(post_save, sender=CarResale)
def post_save_car_resale(instance: CarResale, created, **kwargs):
    if created:
        car_order: CarOrder = instance.carOrder
        car_order.price = instance.salePrice
        car_order.client = instance.newClient

        balance = instance.newClient.balances.create(
            sum_in_jpy=car_order.total,
            payment_type=Balance.PAYMENT_TYPE_CASHLESS,
            balance_action=Balance.BALANCE_ACTION_WITHDRAWAL,
            sender_name="CarResale",
            comment=f"Withdrawal for resaling car #{car_order.id}",
        )
        car_order.withdrawal.balance = balance
        car_order.save()

        # Calculate balances
        car_order.refresh_from_db()
        balance = instance.oldClient.balances.create(
            sum_in_jpy=car_order.total,
            rate=1,
            sum_in_usa=car_order.total,
            payment_type=Balance.PAYMENT_TYPE_CASHLESS,
            balance_action=Balance.BALANCE_ACTION_REPLENISHMENT,
            sender_name="CarResale",
            comment=f"Replenishment for resaling car#{car_order.id}",
        )
        CarResaleOldClientReplenishment.objects.create(
            balance=balance, car_resale=instance
        )

        if instance.oldClient.username == settings.SANRI_USERNAME:
            income_type, created = IncomeType.objects.get_or_create(
                name="car_resale"
            )
            income_type.incomes.create(
                amount=instance.salePrice - instance.startingPrice
            )

        CarSale.objects.filter(carOrder=car_order).delete()

    instance.old_client_replenishment.calculate()
