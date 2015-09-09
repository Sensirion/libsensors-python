Simple Python Sensor Library
============================

This is a small and simple library to collect data using Sensirion sensors with
Python. Currently the following sensor chips are supported:

* SHT3x (temperature and humidity)
* SF04 (flow and differential pressure chip) used in the following products:
   * SDP6xx Series
   * SFM4xxx Series
   * SLx Series
   * Lx Series
   * LPG Series
* SF05 (flow and differential pressure chip) used in the following products:
   * SFM3xxx Series

Library
-------
The library functions are located in the file sensirion_sensors.py.  The
different functions and classes are documented in the source code.

Examples
--------
The library comes with three examples that show different ways to use the library:

1. sync_example.py
Command line tool that reads all sensors synchronously with the same sampling
frequency. The data can either be plotted to the console or stored in a file.

2. async_example.py
Command line script that reads every sensor asynchronously with an individual
sampling frequency.

3. streaming_example.py and streaming_client.py
An example script that streams all sensor data to a local MQTT broker. The
streaming_client scripts demonstrates how to connect to a remote broker and
subscribe to sensor data.
The format of the MQTT payload is in JSON, an example for an SHT  sensor is
included below. Timestamps are in seconds since 1970.
{
    "timestamp": 1441799806.62,
    "values": [ 24.35, 53.21 ],
    "units": [ "°C", "%" ]
}
