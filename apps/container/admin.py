from django.contrib import admin

from . import models


class CountAndSumInline(admin.StackedInline):
    model = models.CountAndSum
    extra = 0

    def has_add_permission(self, request, obj):
        return request.user.is_superuser 

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser 


@admin.register(models.Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("id", "name") 

    inlines = [CountAndSumInline]
