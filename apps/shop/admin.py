from django.contrib import admin

from .models import ShopCar, ShopImage, FuelEfficiency


class FuelEfficiencyInline(admin.StackedInline):
    model = FuelEfficiency
    extra = 0


class ShopImageInline(admin.StackedInline):
    model = ShopImage
    extra =  0


@admin.register(ShopCar)
class ShopCarAdmin(admin.ModelAdmin):
    inlines = [ FuelEfficiencyInline, ShopImageInline]