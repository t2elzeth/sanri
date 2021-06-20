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

    STATUS_GOING_TO = 'going_to'
    STATUS_SHIPPED = 'shipped'
    STATUS_CHOICES = ((STATUS_GOING_TO, STATUS_GOING_TO),
                      (STATUS_SHIPPED, STATUS_SHIPPED))

    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    totalAmount = models.IntegerField()


class CountAndSum(models.Model):
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="count_and_sum"
    )
    count = models.IntegerField()
    sum = models.IntegerField()
