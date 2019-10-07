# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kevin/Documents/Research/Underwater TOF Camera/Code/CaptureGUI/preview.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic
from Epc660 import *
import cv2
import time
import pyqtgraph as pg
import numpy as np
from numpy import *
import os

# Load the local directory, will be used to find .ui files
LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"

class Ui_PreviewWindow(QMainWindow):
    def setupUi(self, PreviewWindow, camera_index=0, fps=30):
        # Set white background and black foreground
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'w')
        pg.setConfigOptions(imageAxisOrder='col-major')
        self.ui = uic.loadUi(LOCAL_DIR + "preview.ui", self)
        self.show()
        
        self.ui.graphicsViewDCS = pg.ImageView(self.centralwidget)
        self.ui.graphicsViewDCS.setGeometry(QRect(10, 50, 471, 391))
        
        self.ui.graphicsViewDistance = pg.ImageView(self.centralwidget)
        self.ui.graphicsViewDistance.setGeometry(QRect(490, 260, 351, 221))
        
        self.ui.graphicsViewAmplitude = pg.PlotWidget(self.centralwidget)
        self.ui.graphicsViewAmplitude.setGeometry(QRect(490, 10, 351, 221))
#
        self.ui.graphicsViewDCS.show()
        self.ui.graphicsViewDistance.show()
        self.ui.graphicsViewAmplitude.show()

        # self.graphicsViewDCS.ui.histogram.hide()
#        self.ui.graphicsViewDCS.ui.roiBtn.hide()
        self.ui.graphicsViewDCS.ui.menuBtn.hide()

        # self.graphicsViewDistance.ui.histogram.hide()
#        self.ui.graphicsViewDistance.ui.roiBtn.hide()
        self.ui.graphicsViewDistance.ui.menuBtn.hide()
#        
#        self.ui.graphicsViewAmplitude.setXRange(0, 255, padding=0)
        self.ui.graphicsViewAmplitude.setYRange(0, 1, padding=0)
        self.init_camera()
        
    def init_camera(self):
        self.capture = ImageThread()
        self.converter = Converter()
        captureThread = QThread(self)
        converterThread = QThread(self)
        self.converter.setProcessAll(False)
        captureThread.start()
        converterThread.start()
        self.capture.moveToThread(captureThread)
        self.converter.moveToThread(converterThread)
        self.capture.frameReady.connect(self.converter.processFrame)
        self.converter.imageReady.connect(self.display_frame)
        self.capture.started.connect(lambda: print("started"))
        self.ui.pushButtonStart.clicked.connect(self.capture.start)
        self.ui.pushButtonPause.clicked.connect(self.capture.stop)
#        x = np.random.normal(size=1000)
#        y = np.random.normal(size=1000)
#        pg.plot(x, y, pen=None, symbol='o')
    
    def display_frame(self, frame):
        dist_img = self.capture.camera.epc_conn.compute_distance(frame)
        x = np.histogram(dist_img, bins = 255, density=True)

        self.ui.graphicsViewAmplitude.plot(x[1][1::], x[0], pen=pg.mkPen(width=3, color='r'), clear =True)

        dcs_img = np.hstack((np.vstack((frame[0,:,:], frame[2,:,:])), np.vstack((frame[1,:,:], frame[3,:,:]))))

        self.ui.graphicsViewDCS.setImage(dcs_img.T)
        self.ui.graphicsViewDistance.setImage(dist_img.T)
        
    def initUI(self):
        captureThread = QThread(self)
        captureThread.start()
        
class ImageThread(QObject):
    frameReady = pyqtSignal('PyQt_PyObject')
    started = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)
        TCP_IP = '192.168.7.2'
        TCP_PORT = 50660
        TCP_BUFFER = 8192
        TIMEOUT = 5
        self.camera = EpcCam()
        self.camera.set_buffer(TCP_BUFFER)
        self.camera.set_tcp_port(TCP_PORT)
        self.camera.set_tcp_ip(TCP_IP)
        self.m_timer = QBasicTimer()
        self.camera.set_int_time(4000)
        self.camera.set_modulation(0)
    
    def timerEvent(self, event):
        if event.timerId() != self.m_timer.timerId():
            return
        
        dcs_img = self.camera.take_image('dcs')
        self.frameReady.emit(dcs_img)
    
    @pyqtSlot()
    def start(self):
        self.m_timer.start(0, self)
        self.started.emit()
    
    @pyqtSlot()
    def stop(self):
        self.m_timer.stop()
        
class Converter(QObject):
    imageReady = pyqtSignal(ndarray)

    def __init__(self, parent=None):
        super(Converter, self).__init__(parent)
        self.m_frame = np.array([])
        self.m_frame_proc = np.array([])
        self.m_frame_hist = np.array([])
        self.m_timer = QBasicTimer()
        self.m_processAll = True
        self.m_image = np.array([])

    def queue(self, frame):
        self.m_frame = frame
        if not self.m_timer.isActive():
            self.m_timer.start(0, self)

    def process(self, frame):
#        w, h, _ = frame.shape
#        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # dcs_img = np.reshape(frame, [2*240, 2*320])
        # dcs_image = np.reshape(frame, [2*320, 2*240], order = 'C')
        self.m_image = frame
#        self.m_image = QImage(dcs_img, *dcs_img.shape[1::-1], QImage.Format_Grayscale8).rgbSwapped()
#        self.m_image = QImage(rgbImage.data, h, w, QImage.Format_RGB888)
        self.imageReady.emit(self.m_image)

    def timerEvent(self, event):
        if event.timerId() != self.m_timer.timerId():
            return
        self.process(self.m_frame)
        self.m_timer.stop()

    def processAll(self):
        return self.m_processAll

    def setProcessAll(self, _all):
        self.m_processAll = _all

    def processFrame(self, frame):
        if self.m_processAll:
            self.process(frame)
        else:
            self.queue(frame)

    def image(self):
        return self.m_image
    
    def frame_proc(self):
        return self.m_frame_proc
    
    def frame_hist(self):
        return self.m_frame_hist

#    image = pyqtProperty(QImage, fget=image, notify=imageReady, user=True)
    image = pyqtProperty(ndarray, fget=image, notify=imageReady, user=True)
    processAll = pyqtProperty(bool, fget=processAll, fset=setProcessAll)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    PreviewWindow = QMainWindow()
    ui = Ui_PreviewWindow()
    ui.setupUi(PreviewWindow)
    sys.exit(app.exec_())
