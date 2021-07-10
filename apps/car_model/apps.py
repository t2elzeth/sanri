from django.apps import AppConfig


class CarModelConfig(AppConfig):
    """Модель и марка машин"""
    default_auto_field = "django.db.models.BigAutoField"
    name = "car_model"
