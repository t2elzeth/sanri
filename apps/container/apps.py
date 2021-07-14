import importlib

from django.apps import AppConfig


class ContainerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "container"

    def ready(self):
        importlib.import_module(".signals", "container")
        return super().ready()
