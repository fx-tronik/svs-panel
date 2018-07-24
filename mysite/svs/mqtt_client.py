from .models import Infrasctructure
import paho.mqtt.client as mqtt
import json

SUB_TOPICS_CV = ("ws-arm-imp", "ws-arm-cr", "ws-arm-bas")
SUB_TOPICS_ES = ("SVS_callback",)
RECONNECT_DELAY_SECS = 2


# Custom client class to catch exceptions and dump them into ws-debug topic.
# Without it, on excepton the client thread hangs and does not recover untill
# restart
class CustomMqttClient(mqtt.Client):

    def _handle_on_message(self, message):
        try:
            super(CustomMqttClient, self)._handle_on_message(message)
        except Exception as e:
            error = {"exception": str(e.__class__.__name__), "message": str(e)}
            self.publish("ws-debug", json.dumps(error), qos=1)


# The callback for when the client receives a CONNACK response from the server.
def on_connect_CV(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in SUB_TOPICS_CV:
        print(topic)
        client.subscribe(topic, qos=1)


def on_connect_ES(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in SUB_TOPICS_ES:
        print(topic)
        client.subscribe(topic, qos=1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == "SVS_callback":
        print(msg.payload)
        j = json.loads(str(msg.payload.decode("utf-8", "ignore")))
        for group in j:
            print(group)
            for i, value in enumerate(j[group]):
                infrastructure, created = Infrasctructure.objects.get_or_create(type=group, no=i+1)
                infrastructure.value = value
                infrastructure.save()
    elif msg.topic == "ws-arm-cr":
        print(msg.payload)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))
    print('wyslalem')

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mosq, obj, level, string):
    print(string)


def on_disconnect(client, userdata, rc):
    client.loop_stop(force=False)
    if rc != 0:
        print("Unexpected disconnection: rc:" + str(rc))
    else:
        print("Disconnected: rc:" + str(rc))


client = CustomMqttClient()
client.on_connect = on_connect_CV
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect


client2 = CustomMqttClient()
client2.on_connect = on_connect_ES
client2.on_message = on_message
# client2.on_publish = on_publish
client2.on_subscribe = on_subscribe
client2.on_disconnect = on_disconnect
