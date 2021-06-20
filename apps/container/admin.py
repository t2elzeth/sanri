from django.contrib import admin

from . import models


class CountAndSumInline(admin.StackedInline):
    model = models.CountAndSum
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Container)
class ContainerAdmin(admin.ModelAdmin):
    inlines = [CountAndSumInline]
