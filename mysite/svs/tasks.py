from mysite.celery import app
from . import mqtt_client as mqtt


from celery.five import monotonic
from celery.utils.log import get_task_logger
from contextlib import contextmanager
from django.core.cache import cache


logger = get_task_logger(__name__)

LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes


@app.task
def Test():

    mqtt.client.connect('192.168.0.200', 1885, 60)
    mqtt.client.loop_start()


@app.task
def Test1():
    mqtt.client2.connect('192.168.0.200', 1885, 60)
    mqtt.client2.loop_start()

@app.task
def printsomething():
    print('test')
