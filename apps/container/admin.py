from django.contrib import admin

from . import models


class ContainerWheelRecyclingInline(admin.StackedInline):
    model = models.ContainerWheelRecycling
    extra = 0


class ContainerWheelSalesInline(admin.StackedInline):
    model = models.ContainerWheelSales
    extra = 0


@admin.register(models.Container)
class ContainerAdmin(admin.ModelAdmin):
    inlines = [ContainerWheelRecyclingInline, ContainerWheelSalesInline]
