#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Sample app to synchronously read out sensor values.

All sensors are polled with the same frequency as synchronously as possible. The output will be written to the console,
or to an output file, if specified. The sensors are read out on the main thread and the program blocks until cancelled
by a keyboard interrupt.
"""

from sensirion_sensors import find_sensors_by_type, SensorReader

import argparse
import sys
import time


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frequency', '-f', type=int, default=10, help='read out frequency')
    parser.add_argument('log_file', type=argparse.FileType('w'), default=sys.stdout, nargs='?', help='Output file')
    args = parser.parse_args()

    # probe for sensors
    sensors = find_sensors_by_type('sfxx') + find_sensors_by_type('sht3x')
    if not sensors:
        sys.stderr.writelines('No sensors found!\n')
        return

    # set up the printing
    log_file = args.log_file
    if log_file == sys.stdout:
        start = time.time()
        separator = '\t'
        value_format = '{0:.3f} {1}'
        missing_format = 'None {1}'
    else:
        start = 0
        separator = ','
        value_format = '{0:.3f}'
        missing_format = ''

    # print a header
    log_file.write('timestamp[s]{0}'.format(separator))
    log_file.write(separator.join('{0}[{1}]'.format(type(s).__name__, u) for s in sensors for u in s.get_units()))
    log_file.write('\n')

    def print_values(timestamp, values):
        log_file.write(value_format.format(timestamp - start, 's'))
        for sensor, sensor_values in values.iteritems():
            for value, unit in zip(sensor_values, sensor.get_units()):
                log_file.write(separator)
                if value is None:
                    log_file.write(missing_format.format(value, unit))
                else:
                    log_file.write(value_format.format(value, unit))
        log_file.write('\n')
        return True

    # run the sensor reader synchranously
    try:
        reader = SensorReader(sensors, args.frequency, print_values)
        reader.run()
    finally:
        log_file.close()


if __name__ == '__main__':
    main()
