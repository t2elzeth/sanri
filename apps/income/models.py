from django.db import models
from django.utils import timezone


class IncomeType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("id",)


class Income(models.Model):
    type = models.ForeignKey(
        IncomeType, on_delete=models.CASCADE, related_name="incomes"
    )
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    comment = models.TextField(default="")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount}"

    class Meta:
        ordering = ("id",)
