from django.apps import AppConfig


class SvsConfig(AppConfig):
    name = 'svs'
    def ready(self):
        from . import mqtt
        mqtt.client.loop_start()
