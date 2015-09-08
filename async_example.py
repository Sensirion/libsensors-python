#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Sample app to asynchronously read out sensor values.

All sensors are polled on their own thread with individual polling frequencies.The program blocks until cancelled
by a keyboard interrupt.
"""

from sensirion_sensors import find_sensor_by_type, SensorReader

import sys


def main():

    sfm = find_sensor_by_type('sfm3000')
    sdp = find_sensor_by_type('sdp600')
    sht = find_sensor_by_type('sht3x')
    if not all((sfm, sdp, sht)):
        sys.stderr.writelines("couldn't find all sensors\n")
        return

    def print_sensor_values(sensor_name):
        def print_to_console(timestamp, values):
            print "{0}: {1}".format(sensor_name, values.values()[0])
            return True
        return print_to_console

    try:
        sfm_reader = SensorReader((sfm,), 100, print_sensor_values('sfm'))
        sdp_reader = SensorReader((sdp,), 10, print_sensor_values('sdp'))
        sht_reader = SensorReader((sht,), 1, print_sensor_values('sht'))
        sfm_reader.start()
        sdp_reader.start()
        sht_reader.run()
    finally:
        sfm_reader.join()
        sdp_reader.join()

if __name__ == '__main__':
    main()
