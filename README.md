# WiFi-positioning-system

It trilaterates the position of the broker using RSSI values from all the nodes
Based on MQTT protocol and using the log model for calculation distances from RSSI values
Uses kalman filter for filtering out erratic data in real-time (Assumption: External noises are null)

Software:
1. MongoDB
2. Mosquitto Broker

Hardware:
1. NodeMCU as nodes
2. Raspi as server/broker

Modes for failure:
1. Change the AP ssid and pass in the code from all the nodes
2. The mongoDB and mosquitto broker are left open in the project, add pass in code if needed.
3. Keep the server in a relatively open open space to reduce multipath fading
