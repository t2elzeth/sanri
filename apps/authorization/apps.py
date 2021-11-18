from django.apps import AppConfig
import importlib


class AuthorizationConfig(AppConfig):
    name = "authorization"

    def ready(self):
        importlib.import_module(".signals", "authorization")
        return super().ready()
