from django.db import models


class IncomeType(models.Model):
    name = models.CharField(max_length=255)


class Income(models.Model):
    type = models.ForeignKey(
        IncomeType, on_delete=models.CASCADE, related_name="incomes"
    )
    date = models.DateField()
    amount = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return f"{self.amount}"
