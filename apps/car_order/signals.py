from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from authorization.models import Balance
from .models import BalanceWithdrawal, CarOrder


@receiver(pre_save, sender=CarOrder)
def update_stock(instance: CarOrder, **kwargs):
    instance.calculate_totals()


@receiver(post_save, sender=CarOrder)
def post_save_car_resale(instance: CarOrder, created, **kwargs):
    if created:
        balance = Balance.objects.create(
            client=instance.client,
            sum_in_jpy=instance.total,
            payment_type=Balance.PAYMENT_TYPE_CASHLESS,
            sender_name="CarOrder",
            comment=f"Balance withdrawal for CarOrder#{instance.id}",
            balance_action=Balance.BALANCE_ACTION_WITHDRAWAL,
        )
        BalanceWithdrawal.objects.create(balance=balance, car_order=instance)
        instance.save()

    instance.withdrawal.calculate_amount()


@receiver(post_delete, sender=BalanceWithdrawal)
def post_delete_balance_withdrawal(instance: BalanceWithdrawal, **kwargs):
    instance.balance.delete()
