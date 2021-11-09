from django.db import models
from car_model.models import CarModel
from authorization.models import User


class Car(models.Model):
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year = models.IntegerField()
    volume = models.DecimalField(max_digits=4, decimal_places=2)
    mileage = models.DecimalField(max_digits=20, decimal_places=2)
    condition = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.model.mark.name} | {self.model.name} for {self.price}"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField()


class BuyRequest(models.Model):
    from_client = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="buy_requests")

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_DECLINED = "declined"
    STATUS_CHOICES = ((STATUS_PENDING, STATUS_PENDING),
                      (STATUS_APPROVED, STATUS_APPROVED),
                      (STATUS_DECLINED, STATUS_DECLINED))
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=STATUS_PENDING)
