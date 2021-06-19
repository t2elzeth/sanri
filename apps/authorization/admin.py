from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from . import models


# class UserAdmin(BaseUserAdmin):
#     # ordering = ("is_staff",)
#     #
#     # list_display = ("email",)
#     #
#     # list_filter = ("is_staff",)
#     #
#     # readonly_fields = ("id", "is_superuser", "is_staff")
#     # add_fieldsets = (
#     #     ("Personal data", {"fields": ("first_name", "last_name")}),
#     #     (
#     #         "Authentication data",
#     #         {
#     #             "classes": ("wide",),
#     #             "fields": ("email", "password1", "password2"),
#     #         },
#     #     ),
#     # )
#
#     # fieldsets = (
#     #     (
#     #         "User data",
#     #         {
#     #             "fields": (
#     #                 "id",
#     #                 "first_name",
#     #                 "last_name",
#     #                 "email",
#     #                 "is_superuser",
#     #                 "is_staff",
#     #                 "is_active",
#     #             )
#     #         },
#     #     ),
#     # )
#     pass


admin.site.register(models.User)

admin.site.unregister(Group)
