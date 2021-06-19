from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ContainerWheelRecycling(models.Model):
    count = models.IntegerField()
    sum = models.IntegerField()


class ContainerWheelSales(models.Model):
    count = models.IntegerField()
    sum = models.IntegerField()


class Container(models.Model):
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="containers"
    )
    name = models.CharField(max_length=255)
    dateOfSending = models.DateField()
    commission = models.IntegerField()
    containerTransportation = models.IntegerField()
    packagingMaterials = models.IntegerField()
    transportation = models.IntegerField()
    loading = models.IntegerField()
    wheelRecycling = models.ForeignKey(
        ContainerWheelRecycling,
        on_delete=models.CASCADE,
        related_name="wheel_recycling",
    )
    wheelSales = models.ForeignKey(
        ContainerWheelSales,
        on_delete=models.CASCADE,
        related_name="wheel_sales",
    )
    status = models.IntegerField()
    totalAmount = models.IntegerField()
