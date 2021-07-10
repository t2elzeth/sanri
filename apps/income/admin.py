from django.contrib import admin

from .models import Income, IncomeType


class IncomeInline(admin.StackedInline):
    model = Income
    extra = 0


@admin.register(IncomeType)
class IncomeTypeAdmin(admin.ModelAdmin):
    inlines = [IncomeInline]
