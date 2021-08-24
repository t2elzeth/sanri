from django.apps import AppConfig

import importlib


class ShopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shop"

    def ready(self):
        importlib.import_module(".signals", "container")
        return super().ready()
