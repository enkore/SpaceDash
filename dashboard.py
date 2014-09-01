# -*- coding: utf-8 -*-
import sys
import json
import urllib.request
import threading
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *


class UpdateThread(threading.Thread):

    def __init__(self):
        super(UpdateThread, self).__init__()
        self.app = QGuiApplication(sys.argv)
        self.view = QQuickView()
        self.view.setWidth(1024)
        self.view.setHeight(600)
        self.view.setTitle("SpaceApi Dashboard")
        self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.view.setSource(QUrl('dashboard.qml'))
        self.view.show()
        self.qml_rectangle = self.view.rootObject()
        self.qml_rectangle.updateTemperature("Running")

    def run(self):
        while True:
            time.sleep(1.0)
            bytedata = urllib.request.urlopen('http://status.hasi.it/spaceapi').read()
            stringdata = bytedata.decode("utf-8")
            jsondata = json.loads(stringdata)
            currentTemperature = str(jsondata['sensors']['temperature'][0]['value']) + " " + jsondata['sensors']['temperature'][0]['unit']
            self.qml_rectangle.updateTemperature(currentTemperature)


t = UpdateThread()
t.start()

sys.exit(t.app.exec_())