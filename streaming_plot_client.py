#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Sample appplication that connects to a mqtt server and plots all sensor data.

It is possible to subscribe to only some sensors or to all of them by modifying
the subscription topic.

To run the script you need to install the paho MQTT library and PyQt as listed
in requirements.txt.
"""

from collections import deque
import json

from PyQt4 import QtCore, QtGui, Qt
from PyQt4.Qwt5 import QwtPlot, QwtPlotCurve, QwtLegend
import paho.mqtt.client as mqtt

MAX_LENGTH = 1000
LEGENDS = {
    'sl/min': 'Flow',
    'Pa': 'Differential Pressure',
    u'°C': 'Temperature',
    '%': 'Humidity'
}


class PlotWindow(QtGui.QMainWindow):
    client_message = QtCore.pyqtSignal(object)
    colors = (
        Qt.Qt.red,
        Qt.Qt.blue,
        Qt.Qt.magenta,
        Qt.Qt.darkCyan,
        Qt.Qt.yellow,
        Qt.Qt.green,
    )
    color_index = -1

    def __init__(self, mqtt_client):
        super(PlotWindow, self).__init__()
        self._plots = {}
        # Create the GUI refresh timer
        self._mqtt_client = mqtt_client
        self._first_timestamp = None
        self.setup_ui()

    def next_color(self):
        self.color_index += 1
        if self.color_index == len(self.colors):
            self.color_index = 0
        return self.colors[self.color_index]

    def setup_ui(self):
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.setWindowTitle('Sensirion Plot')
        central_widget = QtGui.QWidget(self)
        central_widget.setObjectName("centralwidget")
        self.vertical_layout = QtGui.QVBoxLayout(central_widget)
        self.vertical_layout.setObjectName("verticalLayout")
        self.setCentralWidget(central_widget)
        # hook events
        self._mqtt_client.on_connect = self.on_connect
        # we need the signal so the event is processed on the GUI thread
        self._mqtt_client.on_message = lambda c, d, msg: self.client_message.emit(msg)
        self.client_message.connect(self.on_client_message)

    def on_client_message(self, message):
        payload = json.loads(message.payload)
        sensor = message.topic.split('/')[-2]
        if not sensor in self._plots:
            self.add_plot(sensor, payload['units'])
        if not self._first_timestamp:
            self._first_timestamp = payload['timestamp']
        plot = self._plots[sensor]
        plot.time.append(payload['timestamp'] - self._first_timestamp)
        for i, value in enumerate(payload['values']):
            plot.data[i].append(value)
            plot.curves[i].setData(list(plot.time), list(plot.data[i]))
        plot.replot()
        return

    def add_plot(self, name, units):
        # legend
        legend = QwtLegend()
        legend.setFrameStyle(Qt.QFrame.Box | Qt.QFrame.Sunken)
        legend.setItemMode(QwtLegend.ClickableItem)
        # plot
        plot = QwtPlot(self)
        plot.setTitle(name.upper())
        plot.setObjectName(name)
        plot.setCanvasBackground(Qt.Qt.white)
        plot.setAxisTitle(QwtPlot.xBottom, "time [s]")
        plot.insertLegend(legend, QwtPlot.RightLegend)
        plot.time = deque(maxlen=MAX_LENGTH)
        plot.data = []
        plot.curves = []
        for i, unit in enumerate(units):
            position = QwtPlot.yLeft if i == 0 else QwtPlot.yRight
            curve = QwtPlotCurve(LEGENDS[unit])
            curve.setPen(Qt.QPen(self.next_color(), 2))
            curve.setYAxis(position)
            curve.attach(plot)
            plot.enableAxis(position)
            plot.setAxisTitle(position, unit)
            plot.curves.append(curve)
            plot.data.append(deque(maxlen=MAX_LENGTH))
        self.vertical_layout.addWidget(plot)
        self._plots[name] = plot

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.

        # this subscribes only to the sfm sensor
        # client.subscribe("sensors/+/sfm/#")
        # this subscribes to all sensors
        client.subscribe("sensors/#")


if __name__ == "__main__":
    import sys

    client = mqtt.Client()
    app = QtGui.QApplication(sys.argv)
    mainWindow = PlotWindow(client)
    mainWindow.show()

    client.connect("192.168.1.10")
    client.loop_start()
    try:
        sys.exit(app.exec_())
    finally:
        client.loop_stop()
