from django.db import models


class StaffExpenseType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("id",)


class StaffMember(models.Model):
    full_name = models.CharField(max_length=255)
    visa = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    visa_expiration_date = models.DateField()

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ("id",)


class StaffExpense(models.Model):
    staff_member = models.ForeignKey(
        StaffMember, on_delete=models.CASCADE, related_name="expenses"
    )
    type = models.ForeignKey(
        StaffExpenseType,
        on_delete=models.CASCADE,
        related_name="staff_expenses",
    )
    date = models.DateField()
    amount = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return f"{self.amount}"

    class Meta:
        ordering = ("id",)
