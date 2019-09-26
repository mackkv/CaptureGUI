# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kevin/Documents/Research/Underwater TOF Camera/Code/CaptureGUI/preview.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Epc660 import *
import cv2
import time
import pyqtgraph as pg
import numpy as np
from numpy import *

class Ui_PreviewWindow(QWidget):
    def setupUi(self, PreviewWindow, camera_index=0, fps=30):
        PreviewWindow.setObjectName("PreviewWindow")
        PreviewWindow.resize(1188, 557)
        
        # Set white background and black foreground
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'w')
        pg.setConfigOptions(imageAxisOrder='col-major')
        
        self.centralwidget = QWidget(PreviewWindow)
        self.centralwidget.setObjectName("centralwidget")
        
#        self.graphicsViewDCS = QGraphicsView(self.centralwidget)
        # self.graphicsViewDCS = QLabel(self.centralwidget)
        self.graphicsViewDCS = pg.ImageView(self.centralwidget)
        # self.graphicsViewDCS = pg.ImageItem(self.centralwidget)
        self.graphicsViewDCS.setGeometry(QRect(10, 50, 471, 391))
        self.graphicsViewDCS.setObjectName("graphicsViewDCS")
#        self.graphicsViewDistance = QGraphicsView(self.centralwidget)
        # self.graphicsViewDistance = QLabel(self.centralwidget)
        self.graphicsViewDistance = pg.ImageView(self.centralwidget)
        self.graphicsViewDistance.setGeometry(QRect(490, 260, 351, 221))
        self.graphicsViewDistance.setObjectName("graphicsViewDistance")
#        self.graphicsViewAmplitude = QGraphicsView(self.centralwidget)
        self.graphicsViewAmplitude = pg.PlotWidget(self.centralwidget)
        self.graphicsViewAmplitude.setGeometry(QRect(490, 10, 351, 221))
        self.graphicsViewAmplitude.setObjectName("graphicsViewAmplitude")

        self.graphicsViewDCS.show()
        self.graphicsViewDistance.show()
        self.graphicsViewAmplitude.show()

        # self.graphicsViewDCS.ui.histogram.hide()
        self.graphicsViewDCS.ui.roiBtn.hide()
        self.graphicsViewDCS.ui.menuBtn.hide()

        # self.graphicsViewDistance.ui.histogram.hide()
        self.graphicsViewDistance.ui.roiBtn.hide()
        self.graphicsViewDistance.ui.menuBtn.hide()
        
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QRect(849, 9, 341, 301))
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QRect(9, 19, 321, 281))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        
        self.comboBoxModFrequency = QComboBox(self.gridLayoutWidget)
        self.comboBoxModFrequency.setObjectName("comboBoxModFrequency")
        self.gridLayout.addWidget(self.comboBoxModFrequency, 4, 1, 1, 1)
        self.labelModFrequency = QLabel(self.gridLayoutWidget)
        self.labelModFrequency.setObjectName("labelModFrequency")
        self.gridLayout.addWidget(self.labelModFrequency, 4, 0, 1, 1)
        self.lineEditIntTime = QLineEdit(self.gridLayoutWidget)
        self.lineEditIntTime.setObjectName("lineEditIntTime")
        self.gridLayout.addWidget(self.lineEditIntTime, 2, 1, 1, 1)
        self.labelIntTime = QLabel(self.gridLayoutWidget)
        self.labelIntTime.setObjectName("labelIntTime")
        self.gridLayout.addWidget(self.labelIntTime, 2, 0, 1, 1)
        self.labelModType = QLabel(self.gridLayoutWidget)
        self.labelModType.setObjectName("labelModType")
        self.gridLayout.addWidget(self.labelModType, 3, 0, 1, 1)
        self.labelMaxDistance = QLabel(self.gridLayoutWidget)
        self.labelMaxDistance.setObjectName("labelMaxDistance")
        self.gridLayout.addWidget(self.labelMaxDistance, 5, 0, 1, 1)
        self.labelMinDistance = QLabel(self.gridLayoutWidget)
        self.labelMinDistance.setObjectName("labelMinDistance")
        self.gridLayout.addWidget(self.labelMinDistance, 6, 0, 1, 1)
        self.comboBoxModType = QComboBox(self.gridLayoutWidget)
        self.comboBoxModType.setObjectName("comboBoxModType")
        self.gridLayout.addWidget(self.comboBoxModType, 3, 1, 1, 1)
        self.lineEditMinDistance = QLineEdit(self.gridLayoutWidget)
        self.lineEditMinDistance.setObjectName("lineEditMinDistance")
        self.gridLayout.addWidget(self.lineEditMinDistance, 6, 1, 1, 1)
        self.lineEditMaxDistance = QLineEdit(self.gridLayoutWidget)
        self.lineEditMaxDistance.setObjectName("lineEditMaxDistance")
        self.gridLayout.addWidget(self.lineEditMaxDistance, 5, 1, 1, 1)
        
        # Buttons
        self.pushButtonStart = QPushButton(self.gridLayoutWidget)
        self.pushButtonStart.setObjectName("pushButtonStart")
        self.gridLayout.addWidget(self.pushButtonStart, 7, 0, 1, 1)
#        self.pushButtonStart.clicked.connect(self.on_click_start, fps)
        
        self.pushButtonPause = QPushButton(self.gridLayoutWidget)
        self.pushButtonPause.setObjectName("pushButtonPause")
#        self.pushButtonPause.clicked.connect(self.on_click_pause)
        self.gridLayout.addWidget(self.pushButtonPause, 7, 1, 1, 1)
        
        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QRect(690, 230, 151, 25))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        PreviewWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(PreviewWindow)
        self.menubar.setGeometry(QRect(0, 0, 1188, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAdd_Device = QMenu(self.menuFile)
        self.menuAdd_Device.setObjectName("menuAdd_Device")
        PreviewWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(PreviewWindow)
        self.statusbar.setObjectName("statusbar")
        PreviewWindow.setStatusBar(self.statusbar)
        self.actionLoad_Experiment = QAction(PreviewWindow)
        self.actionLoad_Experiment.setObjectName("actionLoad_Experiment")
        self.actionEpc660 = QAction(PreviewWindow)
        self.actionEpc660.setObjectName("actionEpc660")
        self.actionWebcam = QAction(PreviewWindow)
        self.actionWebcam.setObjectName("actionWebcam")
        self.menuAdd_Device.addAction(self.actionEpc660)
        self.menuAdd_Device.addAction(self.actionWebcam)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuAdd_Device.menuAction())
        self.menuFile.addAction(self.actionLoad_Experiment)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(PreviewWindow)
        QMetaObject.connectSlotsByName(PreviewWindow)
        # self.graphicsViewAmplitude.setXRange(0, 255, padding=0)
        self.graphicsViewAmplitude.setYRange(0, 1, padding=0)
        self.init_camera()

    def retranslateUi(self, PreviewWindow):
        _translate = QCoreApplication.translate
        PreviewWindow.setWindowTitle(_translate("PreviewWindow", "Preview Window"))
        self.groupBox.setTitle(_translate("PreviewWindow", "Controls"))
        self.labelModFrequency.setText(_translate("PreviewWindow", "Modulation Frequency:"))
        self.labelIntTime.setText(_translate("PreviewWindow", "Integration Time:"))
        self.labelModType.setText(_translate("PreviewWindow", "Modulation Type:"))
        self.labelMaxDistance.setText(_translate("PreviewWindow", "Maximum Distance [cm]:"))
        self.labelMinDistance.setText(_translate("PreviewWindow", "Minimum Distance [cm]:"))
        self.pushButtonStart.setText(_translate("PreviewWindow", "Start"))
        self.pushButtonPause.setText(_translate("PreviewWindow", "Pause"))
        self.comboBox_2.setItemText(0, _translate("PreviewWindow", "Distance"))
        self.comboBox_2.setItemText(1, _translate("PreviewWindow", "Amplitude"))
        self.menuFile.setTitle(_translate("PreviewWindow", "File"))
        self.menuAdd_Device.setTitle(_translate("PreviewWindow", "Add Device"))
        self.actionLoad_Experiment.setText(_translate("PreviewWindow", "Load Experiment"))
        self.actionEpc660.setText(_translate("PreviewWindow", "Epc660"))
        self.actionWebcam.setText(_translate("PreviewWindow", "Webcam"))
        
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
        self.pushButtonStart.clicked.connect(self.capture.start)
        self.pushButtonPause.clicked.connect(self.capture.stop)
    
    def display_frame(self, frame):
        dist_img = self.capture.camera.epc_conn.compute_distance(frame)
        x = np.histogram(dist_img, bins = 100, density=True)

        self.graphicsViewAmplitude.plot(x[1][1::], x[0], pen=pg.mkPen(width=3, color='r'), clear =True)

        dcs_img = np.hstack((np.vstack((frame[0,:,:], frame[2,:,:])), np.vstack((frame[1,:,:], frame[3,:,:]))))

        self.graphicsViewDCS.setImage(dcs_img.T)
        self.graphicsViewDistance.setImage(dist_img.T)
        
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
    app = QApplication(sys.argv)
    PreviewWindow = QMainWindow()
    ui = Ui_PreviewWindow()
    ui.setupUi(PreviewWindow)
    PreviewWindow.show()
    sys.exit(app.exec_())
