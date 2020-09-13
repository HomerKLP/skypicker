from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'skypicker.app'

    def ready(self):
        from .tasks import load_flights
        load_flights()

