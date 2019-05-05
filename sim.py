from random import randint

import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
	print("connected with result code " + str(rc))


def on_message(client, userdata, msg):
	message = str(msg.payload.decode("UTF-8"))
	print(msg.topic + " " + message)


def on_publish(mosq, obj, mid):
	print("mid: " + str(mid))


client = mqtt.Client("python")
client.on_connect = on_connect
client.connect("0.0.0.0", 1883, 60)
client.loop_start()

while True:
	client.publish("node1", str(randint(-80, -40)))
	client.publish("node2", str(randint(-80, -40)))
	client.publish("node3", str(randint(-80, -40)))
	client.on_message = on_message
	time.sleep(0.05)
