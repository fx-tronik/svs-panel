from mysite.celery import app
from . import mqtt_client as mqtt
from time import sleep
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


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


@app.task
def mqtt_send(topic, payload):

    send_client = mqtt.CustomMqttClient()
    send_client.connect('192.168.0.200', 1885, 60)
    send_client.publish(topic, payload, qos=1, retain=True)
    sleep(0.1)
    send_client.disconnect()
