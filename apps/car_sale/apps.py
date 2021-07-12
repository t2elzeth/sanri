import importlib

from django.apps import AppConfig


class CarSaleConfig(AppConfig):
    """Продажа машин"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "car_sale"

    def ready(self):
        importlib.import_module(".signals", "car_sale")
        return super().ready()
