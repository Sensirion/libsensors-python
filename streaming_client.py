#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Sample app that connects to a mqtt server and prints all sensor data.

It is possible to subscribe to only some sensors or to all of them.The program
blocks until cancelled by a keyboard interrupt.

To run the script you need to install the paho MQTT library:
pip install paho-mqtt
http://www.eclipse.org/paho/clients/python/docs/
"""
import json
import signal
import sys
import paho.mqtt.client as mqtt

client = mqtt.Client()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    # this subscribes only to the sfm sensor
    #client.subscribe("sensors/+/sfm/#")
    # this subscribes to all sensors
    client.subscribe("sensors/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    sys.stdout.write('{0}, {1}: '.format(msg.topic, payload['timestamp']))
    for v, u in zip(payload['values'], payload['units']):
        sys.stdout.write(u'{0} {1}  '.format(v, u))
    sys.stdout.write('\n')


def signal_handler(signal, frame):
    print('terminating')
    client.disconnect()

signal.signal(signal.SIGINT, signal_handler)
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.1.10")

client.loop_forever()
