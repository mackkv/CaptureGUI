#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 00:22:57 2019

@author: kevin
"""
import cv2
import numpy as np
import PyQt5 import QtCore, QtGui, QtWidgets
from Epc660 import *


class ImageThread(QThread, camera):
    signal = pyqtSignal('PyQt_PyObject')
    
    def __init__(self, camera):
        QThread.__init__(self, camera)
        
    def run(self, camera):
         dcs_img = camera.take_image('dcs')
         self.signal.emit(dcs_img)