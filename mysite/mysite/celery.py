from __future__ import absolute_import
import os
from celery import Celery
from celery.signals import celeryd_init


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@celeryd_init.connect()
def testujemy(conf=None, **kwargs):

    from svs import mqtt_client as mqtt
    mqtt.client.loop_stop()
    mqtt.client.connect('192.168.0.200', 1885, 60)
    mqtt.client.loop_start()

    mqtt.client2.loop_stop()
    mqtt.client2.connect('192.168.0.200', 1885, 60)
    mqtt.client2.loop_start()
