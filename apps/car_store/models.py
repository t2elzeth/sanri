from django.db import models


class CarStore(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    milage = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    displacement = models.CharField(max_length=255)
    complect = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.brand


class CarStoreImage(models.Model):
    car_store = models.ForeignKey(CarStore, on_delete=models.CASCADE, related_name='images')
    name = models.ImageField()

    def __str__(self):
        return self.name
