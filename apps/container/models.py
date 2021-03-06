from car_order.models import CarOrder
from django.contrib.auth import get_user_model
from django.db import models

from .formulas import calculate_total

User = get_user_model()


class Container(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="containers",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    dateOfSending = models.DateField()
    commission = models.IntegerField()
    containerTransportation = models.IntegerField()
    packagingMaterials = models.IntegerField()
    transportation = models.IntegerField()
    loading = models.IntegerField()

    STATUS_GOING_TO = "going_to"
    STATUS_SHIPPED = "shipped"
    STATUS_CHOICES = (
        (STATUS_GOING_TO, STATUS_GOING_TO),
        (STATUS_SHIPPED, STATUS_SHIPPED),
    )

    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    totalAmount = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    def calculate_total(self):
        wheel_recycling = getattr(self, "wheel_recycling", None)
        wheel_sales = getattr(self, "wheel_sales", None)
        self.totalAmount = calculate_total(
            self.commission,
            self.containerTransportation,
            self.packagingMaterials,
            getattr(wheel_recycling, "sum", 0),
            getattr(wheel_sales, "sum", 0),
        )

    class Meta:
        ordering = ("id",)


class WheelRecycling(models.Model):
    container = models.OneToOneField(
        Container, on_delete=models.CASCADE, related_name="wheel_recycling"
    )
    count = models.IntegerField()
    sum = models.IntegerField()

    class Meta:
        ordering = ("id",)


class WheelSales(models.Model):
    container = models.OneToOneField(
        Container, on_delete=models.CASCADE, related_name="wheel_sales"
    )
    count = models.IntegerField()
    sum = models.IntegerField()

    class Meta:
        ordering = ("id",)


class ContainerCar(models.Model):
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="container_cars"
    )
    car = models.ForeignKey(
        CarOrder, on_delete=models.CASCADE, related_name="container_cars"
    )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.container.name}: {self.car.carModel.name}"

    class Meta:
        ordering = ("id",)


class ContainerBalanceWithdrawal(models.Model):
    balance = models.OneToOneField(
        "authorization.Balance",
        on_delete=models.CASCADE,
        related_name="container_withdrawal",
    )
    container = models.OneToOneField(
        Container,
        on_delete=models.CASCADE,
        related_name="container_withdrawal",
    )

    def calculate(self):
        self.balance.sum_in_jpy = self.container.totalAmount
        self.balance.save()

    class Meta:
        ordering = ("id",)
