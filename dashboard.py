# -*- coding: utf-8 -*-
import sys
import json
import urllib.request
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *


class Dashboard(QObject):

    temperatureUpdated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.view = QQuickView()
        self.view.setWidth(1024)
        self.view.setHeight(600)
        self.view.setTitle("SpaceApi Dashboard")
        self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.view.setSource(QUrl('dashboard.qml'))
        self.view.show()
        self.qmlRoot = self.view.rootObject()

        self.update_thread = QThread()
        self.update_timer = QTimer()
        self.update_timer.moveToThread(self.update_thread)
        self.update_timer.setInterval(1000)
        self.update_timer.timeout.connect(self.update)
        self.update_thread.started.connect(self.update_timer.start)
        self.update_thread.start()

        self.temperatureUpdated.connect(self.qmlRoot.updateTemperature)

    @pyqtSlot()
    def update(self):
        print("Updating")

        try:
            bytedata = urllib.request.urlopen('http://status.hasi.it/spaceapi', None, 10).read()
            stringdata = bytedata.decode("utf-8")
            jsondata = json.loads(stringdata)
            self.currentTemperature = str(jsondata['sensors']['temperature'][0]['value']) + " "
            self.currentTemperature += jsondata['sensors']['temperature'][0]['unit']
            self.temperatureUpdated.emit("Temperatur: " + self.currentTemperature)
        except Exception as e:
            self.temperatureUpdated.emit("Temperatur: Error")
            print(e)


app = QGuiApplication(sys.argv)
board = Dashboard()
sys.exit(app.exec_())
