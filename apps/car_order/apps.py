from django.apps import AppConfig


class CarOrderConfig(AppConfig):
    """Покупка машины"""
    default_auto_field = "django.db.models.BigAutoField"
    name = "car_order"
