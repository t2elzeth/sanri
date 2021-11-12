from django.db import models


class CarMark(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)


class CarModel(models.Model):
    mark = models.ForeignKey(
        CarMark, on_delete=models.CASCADE, related_name="models"
    )
    name = models.CharField(max_length=255)

    @property
    def model_name(self):
        return f"{self.mark.name} {self.name}"

    def __str__(self):
        return f"{self.mark}:{self.name}"

    class Meta:
        ordering = ("id",)
