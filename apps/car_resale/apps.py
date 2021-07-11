import importlib

from django.apps import AppConfig


class CarResaleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "car_resale"

    def ready(self):
        importlib.import_module('.signals', 'car_resale')
        return super().ready()
