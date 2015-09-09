#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Sample app to asynchronously read out sensor values and stream the measurements over mqtt.

All sensors are polled on their own thread with individual polling frequencies.The program
blocks until cancelled by a keyboard interrupt.
"""
import time

from sensirion_sensors import find_sensor_by_type, SensorReader

import json
import paho.mqtt.client as mqtt
import signal
import socket
import sys


def on_connect(client, userdata, rc):
    print("Connected with result code {0}".format(rc))
    # Subscribe here to any topics that you are interested in


def main():
    print('detecting sensors')
    sfm = find_sensor_by_type('sfm3000')
    sdp = find_sensor_by_type('sdp600')
    sht = find_sensor_by_type('sht3x')
    if not any((sfm, sdp, sht)):
        sys.stderr.writelines("couldn't find any sensors\n")
        return

    print('connecting to mqtt')
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("localhost")

    def send_sensor_values(sensor, sensor_name):
        topic = 'sensors/{0}/{1}/values'.format(socket.gethostname(), sensor_name)
        units = sensor.get_units()

        def send(timestamp, values):
            measurements = values.values()[0]
            if all(m is not None for m in measurements):
                payload = {
                    "timestamp": timestamp,
                    "values": measurements,
                    "units": units,
                }
                client.publish(topic, json.dumps(payload))
        return send

    def signal_handler(signal, frame):
        print('terminating')
        client.disconnect()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        if sfm:
            sfm_reader = SensorReader((sfm,), 100, send_sensor_values(sfm, 'sfm'))
            sfm_reader.start()
        if sdp:
            sdp_reader = SensorReader((sdp,), 10, send_sensor_values(sdp, 'sdp'))
            sdp_reader.start()
        if sht:
            sht_reader = SensorReader((sht,), 1, send_sensor_values(sht, 'sht'))
            sht_reader.start()
        client.loop_forever()
    finally:
        client.loop_stop()
        if sfm:
            sfm_reader.join()
        if sdp:
            sdp_reader.join()
        if sht:
            sht_reader.join()


if __name__ == '__main__':
    main()
