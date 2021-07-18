from django.db import models

from django.utils import timezone


class IncomeType(models.Model):
    name = models.CharField(max_length=255)


class Income(models.Model):
    type = models.ForeignKey(
        IncomeType, on_delete=models.CASCADE, related_name="incomes"
    )
    date = models.DateField(default=timezone.now)
    amount = models.IntegerField()
    comment = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount}"
