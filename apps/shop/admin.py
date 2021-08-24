from django.contrib import admin

from .models import ShopCar, ShopImage, FuelEfficiency, CarForApprove


class FuelEfficiencyInline(admin.StackedInline):
    model = FuelEfficiency
    extra = 0


class ShopImageInline(admin.StackedInline):
    model = ShopImage
    extra =  0


class ForApproveInline(admin.StackedInline):
    model = CarForApprove


@admin.register(ShopCar)
class ShopCarAdmin(admin.ModelAdmin):
    inlines = [ FuelEfficiencyInline, ShopImageInline, ForApproveInline]