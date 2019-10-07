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
import constant

# Load the local directory, will be used to find .ui files
LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"

class Ui_PreviewWindow(QMainWindow):
    def setupUi(self, PreviewWindow, camera_index=0, fps=30):
        # Set white background and black foreground
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'w')
        pg.setConfigOptions(imageAxisOrder='col-major')
        self.ui = uic.loadUi(LOCAL_DIR + "preview.ui", self)
        self.experiment = False
        self.show()
        
        self.ui.graphicsViewDCS = pg.ImageView(self.centralwidget)
        self.ui.graphicsViewDCS.setGeometry(QRect(10, 10, 471, 391))
        
        self.ui.graphicsViewDistance = pg.ImageView(self.centralwidget)
        self.ui.graphicsViewDistance.setGeometry(QRect(490, 260, 351, 221))
        
        self.ui.graphicsViewAmplitude = pg.PlotWidget(self.centralwidget)
        self.ui.graphicsViewAmplitude.setGeometry(QRect(490, 10, 351, 221))
#
        self.ui.graphicsViewDCS.show()
        self.ui.graphicsViewDistance.show()
        self.ui.graphicsViewAmplitude.show()
        
        self.ui.imageTypeSelect.activated[str].connect(self.imageTypeSelection)
        self.imageType = None

        # self.graphicsViewDCS.ui.histogram.hide()
#        self.ui.graphicsViewDCS.ui.roiBtn.hide()
        self.ui.graphicsViewDCS.ui.menuBtn.hide()

        # self.graphicsViewDistance.ui.histogram.hide()
#        self.ui.graphicsViewDistance.ui.roiBtn.hide()
        self.ui.graphicsViewDistance.ui.menuBtn.hide()
#        
#        self.ui.graphicsViewAmplitude.setXRange(0, 255, padding=0)
        self.ui.graphicsViewAmplitude.setYRange(0, 1, padding=0)
        self.ui.actionLoad_Experiment.triggered.connect(self.openExperimentFileDialog)
        self.ui.actionAdd_Save_Path.triggered.connect(self.saveFileDialog)
        self.init_camera()
    
    def imageTypeSelection(self, text):
        self.imageType = text
        
    def openExperimentFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*.yaml)", options=options)
        if fileName:
            print(fileName)
            self.experiment = True
        
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
        
    def getChoice(self):
        items = ("Red","Blue","Green")
        item, okPressed = QInputDialog.getItem(self, "Get item","Color:", items, 0, False)
        if okPressed and item:
            print(item)
            
    def showDialog(self):
        d = QDialog()
        b1 = QPushButton("ok",d)
        b1.move(50,50)
        d.setWindowTitle("Dialog")
#        d.setWindowModality(ApplicationModal)
        d.exec_()
	
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
        self.converter.imageReady.connect(self.processData)
        self.capture.started.connect(lambda: print("started"))
        self.ui.pushButtonStart.clicked.connect(self.capture.start)
        self.ui.pushButtonPause.clicked.connect(self.capture.stop)
        self.showDialog()
#        x = np.random.normal(size=1000)
#        y = np.random.normal(size=1000)
#        pg.plot(x, y, pen=None, symbol='o')
        
    def processData(self, frame):
        if self.experiment:
            print('save frame, don\'t display')
        else:
            self.displayFrame(frame)
    
    def displayFrame(self, frame):
        dcs_img = np.hstack((np.vstack((frame[0,:,:], frame[2,:,:])), np.vstack((frame[1,:,:], frame[3,:,:]))))

        self.ui.graphicsViewDCS.setImage(dcs_img.T)
        if self.imageType == 'Distance':
            self.ui.graphicsViewDistance.setImage(frame[4,:,:].T)
            x = np.histogram(frame[4, : , :], bins = 255, density=True)
        else:
            self.ui.graphicsViewDistance.setImage(frame[5,:,:].T)
            x = np.histogram(frame[5, : , :], bins = 255, density=True)
            
        self.ui.graphicsViewAmplitude.plot(x[1][1::], x[0], pen=pg.mkPen(width=3, color='r'), clear =True)     
        
        
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
        self.camera.set_int_time(2000)
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
        
class ExperimentThread(QObject):
    
    def __init__(self):
        QThread.__init__(self)
        
class Converter(QObject):
    imageReady = pyqtSignal(ndarray)
    
    def compute_distance(self, dcs_array):
        # dcs_array = np.reshape(np.array(data), (4, constant.CAM_RESX,constant.CAM_RESY))
        f_mod = 12000000 # should be set to getModulationFrequency
        d_offset = 0 # should be set to getOffset
        c = constant.SPEED_OF_LIGHT
        d_tof = (c/2)*(1/(2*np.pi*f_mod))*(np.pi+np.arctan2((dcs_array[3,:,:] - dcs_array[1,:,:]),(dcs_array[2,:,:]-dcs_array[0,:,:]))) + d_offset
        
        # Replace NaN's with 0's
        d_tof = np.nan_to_num(d_tof)
    
        # create "image" with values from 0-255
        # d_img = (d_tof/np.max(d_tof))*constant.MAX_PVALUE
        return d_tof
    
    def compute_amplitude(self, frame):
        raw_max = np.max(frame)
        amp_tof = np.sqrt((frame[2,:,:]-frame[0,:,:])**2/4 + (frame[3,:,:]-frame[1,:,:])**2/4)
        return amp_tof

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
        dist_img = self.compute_distance(frame)
        amp_img = self.compute_amplitude(frame)
        frame = np.concatenate((frame, np.reshape(dist_img, (1, 240, 320))), axis=0)
        frame = np.concatenate((frame, np.reshape(amp_img, (1, 240, 320))), axis=0)
        self.m_image = frame
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
