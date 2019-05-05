import paho.mqtt.client as mqtt
import pymongo
import numpy as np
import time


def on_connect(client, userdata, flags, rc):
	print("connected node1")


def on_message(client, userdata, msg):
	message = int(msg.payload.decode("UTF-8"))
	print(msg.topic, " ", message)
	record(message)


def on_publish(mosq, obj, mid):
	print("mid: " + str(mid))


def record(abc):
	rssi.append(abc)


rssi_calib = -52
samplesPerBlock = 10
rssi = [0]
loss = 3.4

F = np.array([[1, 1], [0, 1]])
x = np.array([[1, 0], [0, 0]])
P = np.array([[1, 0], [0, 1]])
B = np.array([0.5, 1]).T
Kgain = np.array([[0.5, 0], [0, 0.5]])
Q = np.array([[0, 0], [0, 0]])
R = np.array([[1, 0], [0, 1]])

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["miniProject"]
coll = db["node1"]

client = mqtt.Client("py1")
client.on_connect = on_connect
client.connect("0.0.0.0", 1883, 60)
client.subscribe("node1")
client.loop_start()
distStore = []

id = 0
while True:
	j = 0
	mean = 0
	stdDev = 0
	dist = 0
	rssi_count = 0
	rssi = [0]
	rssi_p = 0

	while len(rssi) < samplesPerBlock:
		client.on_message = on_message

	for x in range(samplesPerBlock):
		mean = mean + rssi[x]
	mean = mean / 10
	j += 1

	for x in range(samplesPerBlock):
		stdDev += pow((rssi[x] - mean), 2)
	stdDev = pow((stdDev / 10), 0.5)

	for x in range(samplesPerBlock):
		if rssi[x] < (mean - 0.25 * stdDev) or rssi[x] > -1 * (mean - 0.25 * stdDev):
			rssi[x] = 0
		else:
			rssi_count += 1

	for x in range(samplesPerBlock):
		rssi_p += rssi[x]

	rssi_p = rssi_p / rssi_count
	dist = round(pow(10, ((rssi_calib - rssi_p) / (10 * loss))), 3)

	x = F * x
	P = F * P * np.transpose(F) + Q
	x = x + Kgain@(dist - x)
	coll.insert_one({"id": id, "data": x[0][0]})
	id += 1
