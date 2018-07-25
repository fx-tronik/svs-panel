from django.apps import AppConfig


class SvsConfig(AppConfig):
    name = 'svs'

    def ready(self):

        from . import mqtt_client as mqtt
        from distributedlock import distributedlock
        #with distributedlock('blablabla'):

        mqtt.client.loop_stop()
        mqtt.client.connect('192.168.0.200', 1885, 60)
        mqtt.client.loop_start()

        mqtt.client2.loop_stop()
        mqtt.client2.connect('192.168.0.200', 1885, 60)
        mqtt.client2.loop_start()
