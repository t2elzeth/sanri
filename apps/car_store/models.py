from django.db import models


class CarStore(models.Model):
    brand = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    milage = models.CharField(max_length=255, blank=True, null=True)
    body = models.CharField(max_length=255, blank=True, null=True)
    displacement = models.CharField(max_length=255, blank=True, null=True)
    complect = models.CharField(max_length=255, blank=True, null=True)
    condition = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.brand

    class Meta:
        ordering = ("id",)


class CarStoreImage(models.Model):
    car_store = models.ForeignKey(
        CarStore, on_delete=models.CASCADE, related_name="images"
    )
    name = models.ImageField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)
