from django.contrib.auth import get_user_model
from django.db import models

from car_order.models import CarOrder

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
    totalAmount = models.IntegerField()


class CountAndSum(models.Model):
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="count_and_sum"
    )
    count = models.IntegerField()
    sum = models.IntegerField()


class ContainerCar(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='container_cars')
    car = models.ForeignKey(CarOrder, on_delete=models.CASCADE, related_name='container_cars')

    def __str__(self):
        return f'{self.container.name}: {self.car.carModel.name}'
