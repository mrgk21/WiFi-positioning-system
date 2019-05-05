import pymongo
import json
import threading
import time

indexOverflow = False


def giveDist(index, node):
	if node == 1:
		var = str(node1.find_one({"id": index}))
	if node == 2:
		var = str(node2.find_one({"id": index}))
	if node == 3:
		var = str(node3.find_one({"id": index}))
	var = var.replace("'", "\"")
	var = var.replace("ObjectId(", "")
	var = var.replace(")", "")
	temp = json.loads(var)
	return temp['data']


def checkAgain():
	threading.Timer(1.0, checkAgain).start()
	global indexOverflow
	indexOverflow = False


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["miniProject"]
node1 = db["node1"]
node2 = db["node2"]
node3 = db["node3"]

location = db["location"]

locId = 0
id = 0
d = [0, 0, 0]
x = [0, 0, 4.4]
y = [3, 0, 0]

checkAgain()
while True:
	if not indexOverflow:
		try:
			d[0] = giveDist(id, 1)
			# print(d[0])
			d[1] = giveDist(id, 2)
			# print(d[1])
			d[2] = giveDist(id, 3)
			# print(d[2])
			id += 1

			A = -2*x[0] + 2*x[1]
			B = -2*y[0] + 2*y[1]
			C = pow(d[0], 2) - pow(d[1], 2) - pow(x[0], 2) + pow(x[1], 2) - pow(y[0], 2) + pow(y[1], 2)
			D = -2*x[1] + 2*x[2]
			E = -2*y[1] + 2*y[2]
			F = pow(d[1], 2) - pow(d[2], 2) - pow(x[1], 2) + pow(x[2], 2) - pow(y[1], 2) + pow(y[2], 2)

			xFinal = (C*E - F*B)/(E*A - B*D)
			yFinal = (C*D - A*F)/(B*D - A*E)

			location.insert_one({"id": locId, "x": xFinal, "y": yFinal})
			print("xFinal: ", xFinal)
			print("yFinal: ", yFinal)
			time.sleep(0.1)
			locId += 1

		except:
			indexOverflow = True
		print(indexOverflow)
