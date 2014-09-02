# -*- coding: utf-8 -*-
import sys
import json
import urllib.request
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *
from PyQt5.QtNetwork import *

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
        self.qml_rectangle = self.view.rootObject()

        self.network = QNetworkAccessManager()

        self.update_timer = QTimer()
        self.update_timer.setInterval(1000)
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start()

        self.temperatureUpdated.connect(self.qml_rectangle.updateTemperature)

    @pyqtSlot()
    def update(self):
        reply = self.network.get(QNetworkRequest(QUrl("http://status.mainframe.io/api/spaceInfo")))
        reply.finished.connect(self.process_apidata)

    @pyqtSlot()
    def process_apidata(self):
        reply = self.sender()
        # *hust*
        # schönere lösung wäre wohl eine Membervariable ala pending_reply

        if reply.error():
            print("Network error: {}".format(reply.errorString()))
            self.temperatureUpdated.emit("Temperatur: Error")
            return

        data = reply.readAll().data().decode("utf-8")
        jsondata = json.loads(data)

        self.currentTemperature = str(jsondata['sensors']['temperature'][0]['value']) + " " + jsondata['sensors']['temperature'][0]['unit']
        self.temperatureUpdated.emit("Temperatur: " + self.currentTemperature)



app = QGuiApplication(sys.argv)

board = Dashboard()

sys.exit(app.exec_())
