from django.db import models


class ShopCar(models.Model):
    price = models.IntegerField()

    CURRENCY_USD = "usd"
    CURRENCY_JPY = "jpy"
    CURRENCY_CHOICES = ((CURRENCY_USD, CURRENCY_USD),
                        (CURRENCY_JPY, CURRENCY_JPY),)
    currency = models.CharField(max_length=255, choices=CURRENCY_CHOICES)

    hp = models.IntegerField()
    engine = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.hp}HP | {self.currency}{self.price}"


class FuelEfficiency(models.Model):
    car = models.OneToOneField(ShopCar, on_delete=models.CASCADE, related_name='fuel_efficiency')
    city = models.FloatField()
    track = models.FloatField()

    def __str__(self):
        return f"City:{self.city} | Track: {self.track}"


class ShopImage(models.Model):
    car = models.ForeignKey(ShopCar, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField()

    def __str__(self):
        return f"Image of car #{self.car.id}"