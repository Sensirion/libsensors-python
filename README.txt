Simple Python Sensor Library
----------------------------

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
The library comes with two examples that show different ways to use the library:

1. sync_example.py
Command line tool that reads all sensors synchronously with the same sampling
frequency. The data can either be plotted to the console or stored in a file.

2. async_example.py
Command line script that reads every sensor asynchronously with an individual
sampling frequency.
