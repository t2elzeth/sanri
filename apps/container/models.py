from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

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
    status = models.IntegerField()
    totalAmount = models.IntegerField()


class ContainerWheelRecycling(models.Model):
    container = models.OneToOneField(Container, on_delete=models.CASCADE, related_name='wheelRecycling')
    count = models.IntegerField()
    sum = models.IntegerField()


class ContainerWheelSales(models.Model):
    container = models.OneToOneField(Container, on_delete=models.CASCADE, related_name='wheelSales')
    count = models.IntegerField()
    sum = models.IntegerField()


