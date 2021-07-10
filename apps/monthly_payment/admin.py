from django.contrib import admin

from .models import MonthlyPayment, MonthlyPaymentType


class MonthlyPaymentInline(admin.StackedInline):
    model = MonthlyPayment
    extra = 0


@admin.register(MonthlyPaymentType)
class MonthlyPaymentTypeAdmin(admin.ModelAdmin):
    inlines = [MonthlyPaymentInline]
