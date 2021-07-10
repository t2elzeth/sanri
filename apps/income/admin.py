from django.contrib import admin

from .models import Income, IncomeType


class IncomeTypeInline(admin.StackedInline):
    model = IncomeType
    extra = 0


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    inlines = [IncomeTypeInline]
