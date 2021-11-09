from django.contrib import admin

from . import models


class CarImagesInline(admin.StackedInline):
    model = models.CarImage
    extra = 0


class CarBuyRequestsInline(admin.StackedInline):
    model = models.BuyRequest
    extra = 0


@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):
    inlines = (CarImagesInline, CarBuyRequestsInline)
