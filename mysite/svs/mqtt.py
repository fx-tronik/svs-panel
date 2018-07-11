from .models import Infrasctructure
import paho.mqtt.client as mqtt
import json

from .models import Test

SUB_TOPICS = ("ws-arm-imp", "ws-arm-cr", "ws-arm-bas", "SVS_callback")
RECONNECT_DELAY_SECS = 2


class CustomMqttClient(mqtt.Client):

    def _handle_on_message(self, message):
        try:
            super(CustomMqttClient, self)._handle_on_message(message)
        except Exception as e:
            error = {"exception": str(e.__class__.__name__), "message": str(e)}
            self.publish("SVS_callback", json.dumps(error))

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in SUB_TOPICS:
        client.subscribe(topic, qos=0)


licznik = 0

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    if msg.topic == "SVS_callback":
        j = json.loads(str(msg.payload.decode("utf-8","ignore")))
        for group in j:
            print(group)
            for i, value in enumerate(j[group]):
                infrastructure, created = Infrasctructure.objects.get_or_create(type=group, no=i+1)
                infrastructure.value = value
                infrastructure.save()

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


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
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect

#client.username_pw_set(username, password)
client.connect('192.168.0.200', 1885, 60)
