from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from . import models


class UserAdmin(BaseUserAdmin):
    ordering = ("is_staff",)

    list_display = ("id", "email",)

    list_filter = ("is_staff",)

    readonly_fields = ("id", "is_superuser", "is_staff", "createdAt")
    add_fieldsets = (
        ("Personal data", {"fields": ("fullName", "country", "phoneNumber")}),
        (
            "Authentication data",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "user_type",
                ),
            },
        ),
    )

    fieldsets = (
        (
            "User data",
            {
                "fields": (
                    "id",
                    "fullName",
                    "country",
                    "phoneNumber",
                    "service",
                    "atWhatPrice",
                    "sizeFOB",
                    "username",
                    "role",
                    "createdAt",
                    "user_type",
                    "email",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "password",
                )
            },
        ),
    )


admin.site.register(models.User, UserAdmin)

admin.site.register(models.Balance)
admin.site.register(models.ManagedUser)
admin.site.unregister(Group)
