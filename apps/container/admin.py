from django.contrib import admin

from . import models


class WheelRecyclingInline(admin.StackedInline):
    model = models.WheelRecycling
    extra = 0

    def has_add_permission(self, request, obj):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class WheelSalesInline(admin.StackedInline):
    model = models.WheelSales
    extra = 0

    def has_add_permission(self, request, obj):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class ContainerCarsInline(admin.StackedInline):
    model = models.ContainerCar
    extra = 0


@admin.register(models.Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

    inlines = [WheelRecyclingInline, WheelSalesInline, ContainerCarsInline]
