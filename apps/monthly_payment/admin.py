from django.contrib import admin

from .models import MonthlyPayment, MonthlyPaymentType


class MonthlyPaymentTypeInline(admin.StackedInline):
    model = MonthlyPaymentType
    extra = 0


@admin.register(MonthlyPayment)
class IncomeAdmin(admin.ModelAdmin):
    inlines = [MonthlyPaymentTypeInline]
