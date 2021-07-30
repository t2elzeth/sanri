from django.contrib import admin

from .models import CarMark, CarModel


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 0


@admin.register(CarMark)
class CarMarkAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
