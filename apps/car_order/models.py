from auction.models import Auction
from car_model.models import CarModel
from django.contrib.auth import get_user_model
from django.db import models
from transport_companies.models import TransportCompany
from django.utils import timezone
from .formulas import calculate_total, calculate_total_fob

User = get_user_model()


class CarOrder(models.Model):
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="car_orders", null=True
    )
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="auctions"
    )
    lotNumber = models.CharField(max_length=255, blank=True, null=True)
    carModel = models.ForeignKey(
        CarModel, on_delete=models.CASCADE, related_name="car_orders"
    )
    vinNumber = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField()
    recycle = models.IntegerField()
    auctionFees = models.IntegerField()
    transport = models.IntegerField()
    fob = models.IntegerField()
    amount = models.IntegerField(default=0)
    transportCompany = models.ForeignKey(
        TransportCompany, on_delete=models.CASCADE, related_name="car_orders"
    )

    CAR_NUMBER_REMOVED = "removed"
    CAR_NUMBER_NOT_REMOVED = "not_removed"
    CAR_NUMBER_NOT_GIVEN = "not_given"
    CAR_NUMBER_STATUS_CHOICES = (
        (CAR_NUMBER_REMOVED, CAR_NUMBER_REMOVED),
        (CAR_NUMBER_NOT_REMOVED, CAR_NUMBER_NOT_REMOVED),
        (CAR_NUMBER_NOT_GIVEN, CAR_NUMBER_NOT_GIVEN),
    )
    carNumber = models.CharField(
        max_length=255, choices=CAR_NUMBER_STATUS_CHOICES
    )
    documentsGiven = models.BooleanField(default=False)
    total = models.IntegerField()
    total_FOB = models.IntegerField()
    created_at = models.DateField(default=timezone.now)
    analysis = models.JSONField(default=dict)

    def calculate_totals(self):
        self.total = calculate_total(
            self.price, self.auctionFees, self.recycle, self.transport
        )
        if self.client.atWhatPrice == User.AT_WHAT_PRICE_BY_FOB:
            self.total_FOB = calculate_total_fob(
                self.price, self.amount, self.transport, self.fob
            )
        elif self.client.atWhatPrice == User.AT_WHAT_PRICE_BY_FACT:
            self.total_FOB = 0

    def __str__(self):
        return f"CarOrder#{self.id} of {self.client}"

    class Meta:
        ordering = ("id",)


class BalanceWithdrawal(models.Model):
    balance = models.OneToOneField(
        "authorization.Balance",
        on_delete=models.CASCADE,
        related_name="car_order_withdrawals",
    )
    car_order = models.OneToOneField(
        CarOrder, on_delete=models.CASCADE, related_name="withdrawal"
    )

    def calculate_amount(self):
        self.balance.sum_in_jpy = self.car_order.total
        self.balance.save()

    class Meta:
        ordering = ("id",)
