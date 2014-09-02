# -*- coding: utf-8 -*-
import sys
import json
import urllib.request
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *


class UpdateThread(QThread):

    temperatureUpdated = pyqtSignal(str)

    def __init__(self):
        super(UpdateThread, self).__init__()
        self.view = QQuickView()
        self.view.setWidth(1024)
        self.view.setHeight(600)
        self.view.setTitle("SpaceApi Dashboard")
        self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.view.setSource(QUrl('dashboard.qml'))
        self.view.show()
        self.qml_rectangle = self.view.rootObject()
        self.temperatureUpdated.connect(self.qml_rectangle.updateTemperature)

    def run(self):
        print("Thread starting")
        while True:
            time.sleep(1.0)
            print("Updating")
            try:
                bytedata = urllib.request.urlopen('http://status.hasi.it/spaceapi', None, 10).read()
                stringdata = bytedata.decode("utf-8")
                jsondata = json.loads(stringdata)
                self.currentTemperature = str(jsondata['sensors']['temperature'][0]['value']) + " " + jsondata['sensors']['temperature'][0]['unit']
                self.temperatureUpdated.emit("Temperatur: " + self.currentTemperature)
            except Exception as e:
                self.temperatureUpdated.emit("Temperatur: Error")
                print(e)

app = QGuiApplication(sys.argv)
t = UpdateThread()
t.start()

sys.exit(app.exec_())