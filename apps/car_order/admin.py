from django.contrib import admin

from .models import CarOrder, BalanceWithdrawal, Analysis


class BalanceReplenishmentInline(admin.StackedInline):
    model = BalanceWithdrawal


class AnalysisInline(admin.StackedInline):
    model = Analysis


@admin.register(CarOrder)
class CarOrderAdmin(admin.ModelAdmin):
    inlines = [BalanceReplenishmentInline, AnalysisInline]
