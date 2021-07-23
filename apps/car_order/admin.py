from django.contrib import admin

from .models import CarOrder, BalanceReplenishment


class BalanceReplenishmentInline(admin.StackedInline):
    model = BalanceReplenishment


@admin.register(CarOrder)
class CarOrderAdmin(admin.ModelAdmin):
    inlines = [BalanceReplenishmentInline]
