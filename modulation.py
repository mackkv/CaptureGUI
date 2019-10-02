#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 01:18:39 2019

@author: kevin
"""

import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg

t = np.arange(0.0, 1e-3, 1e-8)
f_c = 24e6
f_mod = 5e3
phi = 0
A = 0.5
m = 1.0

v_amp = (1+m*np.cos(2*np.pi*f_mod*t+phi))*A*np.sin(2*np.pi*f_c*t)

pg.plot(t, v_amp)

c = np.correlate(v_amp.T, v_amp.T, 'full')

pg.plot(c)