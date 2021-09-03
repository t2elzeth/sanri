from django.db import models


class TransportCompany(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ("id",)
