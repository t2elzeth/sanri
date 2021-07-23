from django.contrib import admin

from .models import CarOrder, BalanceWithdrawal


class BalanceReplenishmentInline(admin.StackedInline):
    model = BalanceWithdrawal


@admin.register(CarOrder)
class CarOrderAdmin(admin.ModelAdmin):
    inlines = [BalanceReplenishmentInline]
