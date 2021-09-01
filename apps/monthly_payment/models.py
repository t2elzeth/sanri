from container.models import Container
from django.db import models


class MonthlyPaymentType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)


class MonthlyPayment(models.Model):
    type = models.ForeignKey(
        MonthlyPaymentType,
        on_delete=models.CASCADE,
        related_name="monthly_payments",
    )
    date = models.DateField()
    from_container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="monthly_payments", null=True, blank=True
    )
    amount = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return f"{self.amount}"

    class Meta:
        ordering = ("id",)
