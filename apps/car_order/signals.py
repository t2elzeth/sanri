from authorization.models import Balance
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from authorization.models import User
from django.conf import settings
from .models import BalanceWithdrawal, CarOrder


@receiver(pre_save, sender=CarOrder)
def update_stock(instance: CarOrder, **kwargs):
    if instance.client is not None and instance.client.atWhatPrice in (User.AT_WHAT_PRICE_BY_FOB, User.AT_WHAT_PRICE_BY_FOB2):
        instance.fob = instance.client.sizeFOB
    instance.calculate_totals()


@receiver(post_save, sender=CarOrder)
def post_save_car_resale(instance: CarOrder, created, **kwargs):
    if created:
        withdrawal_amount = 0
        if instance.client.atWhatPrice == User.AT_WHAT_PRICE_BY_FACT:
            withdrawal_amount = instance.total
        elif instance.client.atWhatPrice == User.AT_WHAT_PRICE_BY_FOB:
            withdrawal_amount = instance.total_FOB
        elif instance.client.atWhatPrice == User.AT_WHAT_PRICE_BY_FOB2:
            withdrawal_amount = instance.total_FOB2

            # Withdrawal from Sanri's balance
            sanri = User.objects.get(username=settings.SANRI_USERNAME)
            Balance.objects.create(
                client=sanri,
                sum_in_jpy=(instance.recycle + instance.price * 0.1),
                payment_type=Balance.PAYMENT_TYPE_CASHLESS,
                sender_name="CarOrder",
                comment=f"Снятие за покупку#{instance.id}",
                balance_action=Balance.BALANCE_ACTION_WITHDRAWAL,
            )

        balance = Balance.objects.create(
            client=instance.client,
            sum_in_jpy=withdrawal_amount,
            payment_type=Balance.PAYMENT_TYPE_CASHLESS,
            sender_name="CarOrder",
            comment=f"Снятие за покупку#{instance.id}",
            balance_action=Balance.BALANCE_ACTION_WITHDRAWAL,
        )
        BalanceWithdrawal.objects.create(balance=balance, car_order=instance)
        instance.save()

    instance.withdrawal.calculate_amount()


@receiver(post_delete, sender=BalanceWithdrawal)
def post_delete_balance_withdrawal(instance: BalanceWithdrawal, **kwargs):
    instance.balance.delete()
