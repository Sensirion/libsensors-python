Welcome Hackathon Participants!
===============================

On this page we will collect information relevant to the Breath Hackathon currently gonig on
at Technion in Haifa, Imperial College in London and MIT in Cambridge. Here we will address
any issues that were brought to attention or additional examples that were requested.

Contact / Support
-----------------

Should you have any questions regarding this library or any other component of the Raspberry
Pi that was provided for the hackathon, feel free to contact us through the [GitHub issue
tracker](https://github.com/Sensirion/libsensors-python/issues). During the event, we will
monitor the incoming issues closely.


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

1.  sync_example.py

    Command line tool that reads all sensors synchronously with the same sampling
    frequency. The data can either be plotted to the console or stored in a file.

2.  async_example.py

    Command line script that reads every sensor asynchronously with an individual
    sampling frequency.

3.  streaming_example.py

    An example script that streams all sensor data to a local MQTT broker.
    The format of the MQTT payload is JSON, an example for an SHT  sensor is
    included below. Timestamps are in seconds since 1970.

        {
            "timestamp": 1441799806.62,
            "values": [ 24.35, 53.21 ],
            "units": [ "°C", "%" ]
        }

    The Raspberry Pi you received for the hackathon comes with a preconfigured instance
    of the Mosquitto MQTT broker. There is no setup needed to run this example.

4.  streaming_client.py and streaming_plot_client.py

    These scripts demonstrates how to connect to a remote broker and subscribe to sensor data.
    The streaming_client.py script simply prints all values to the console.
    The streaming_plot_client.py script opens up a window using Qt and shows live plots of all
    sensor values that are streamed.

Further Documentation
---------------------

Current version of this library: https://github.com/Sensirion/libsensors-python

Paho mqtt library reference: http://www.eclipse.org/paho/clients/python/docs/

The Mosquitto MQTT broker: http://mosquitto.org/documentation/

Building the Kernel for Raspberry Pi: https://www.raspberrypi.org/documentation/linux/kernel/building.md
