from django.db import models


class CarMark(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    mark = models.ForeignKey(
        CarMark, on_delete=models.CASCADE, related_name="models"
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.mark}:{self.name}"
