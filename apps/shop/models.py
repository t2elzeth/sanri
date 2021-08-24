from django.db import models
from car_model.models import CarMark, CarModel
from authorization.models import User

class ShopCar(models.Model):
    model = models.ForeignKey(
        CarModel, on_delete=models.CASCADE, related_name="shop_cars"
    )
    price = models.IntegerField()

    CURRENCY_USD = "usd"
    CURRENCY_JPY = "jpy"
    CURRENCY_CHOICES = (
        (CURRENCY_USD, CURRENCY_USD),
        (CURRENCY_JPY, CURRENCY_JPY),
    )
    currency = models.CharField(max_length=255, choices=CURRENCY_CHOICES)

    hp = models.IntegerField()
    engine = models.CharField(max_length=255)
    year = models.IntegerField()
    millage = models.IntegerField()
    condition = models.FloatField()
    body = models.CharField(max_length=255)
    displacement = models.CharField(max_length=255)
    complect = models.CharField(max_length=255)

    STATUS_FOR_SELL = "for_sell"
    STATUS_FOR_APPROVE = "for_approve"
    STATUS_SOLD = "sold"
    STATUS_CHOICES = (
        (STATUS_FOR_SELL, STATUS_FOR_SELL),
        (STATUS_FOR_APPROVE, STATUS_FOR_APPROVE),
        (STATUS_SOLD, STATUS_SOLD),
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_FOR_SELL)

    def __str__(self):
        return f"{self.hp}HP | {self.currency}{self.price}"


class FuelEfficiency(models.Model):
    car = models.OneToOneField(
        ShopCar, on_delete=models.CASCADE, related_name="fuel_efficiency"
    )
    city = models.FloatField()
    track = models.FloatField()

    def __str__(self):
        return f"City:{self.city} | Track: {self.track}"


class ShopImage(models.Model):
    car = models.ForeignKey(
        ShopCar, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField()

    def __str__(self):
        return f"Image of car #{self.car.id}"


class CarForApprove(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE, related_name='for_approve')
    shop_car = models.OneToOneField(ShopCar, on_delete=models.CASCADE, related_name='for_approve')


    def __str__(self):
        return f"For approve car#{self.shop_car.id} from client #{self.client.id}"
