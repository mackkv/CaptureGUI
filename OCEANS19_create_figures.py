#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 15:32:27 2019

@author: kevin
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np

tank_volume = 92.0297514 # calculated in liters using website calculator

# Test relationship between turbidity and maalox prior to Occlusion Experiment
#turbidity = [np.array([0.265, 1.682, 2.974, 4.150, 5.381, 6.671])] # as measured by c-star, this is for blue wavelength
turbidity = [np.array([1.233, 3.128, 4.548, 6.113, 7.658, 8.956])] # this is for green wavelength
maalox    = [np.array([0.000, 0.500, 1.000, 1.500, 2.000, 2.500])/tank_volume] # measured in pipette

# Turbidity data taken during target detection experiment
#turbidity.append([0.475, 1.205, 1.752, 2.355, 2.950, 3.450, 4.489, 5.530, 7.520, 9.620]) # measured by C-Star
turbidity.append([0.740, 1.877, 2.729, 3.668, 4.595, 5.373, 6.992, 8.613, 11.712, 14.983])
maalox.append(np.array([0.000, 0.250, 0.500, 0.750, 1.000, 1.250, 1.750, 2.250, 3.250, 4.250])/tank_volume)# measured in pipette

# Data from Prentice et al.
turbidity.append([0.005, 0.094, 0.162, 0.358,0.752, 1.482, 3.115])
maalox.append([0.0008, 0.0019, 0.0038, 0.0076, 0.0154, 0.0310, 0.0610])

# average target values are taken from a section further down, where the images are segmented by their amplitudes using Otsu's method
avg_target_values = [259.1049, 170.9543, 120.1052, 89.4903, 65.5177, 50.9682, 30.6392827, 20.2716, 11.8543, 10.0000]

#p_0 = 361.3088 # this was measured as the mean value of the return from the target in clear water
p_0 = 434.951
z = 0.7 # this is the distance in meters
c = np.arange(0.7, 15.0, 0.01)
p_z = p_0*np.exp(-c*z)

csfont = {'fontname':'Times New Roman'}
hfont = {'fontname':'Helvetica'}

#plt.rcParams["font.family"] = "Times New Roman"

plt.plot(c*z, p_z, '--', label='Theoretical target amplitude $P_{target} = P_{0}e^{-cz}$', color='black')
plt.plot(np.array(turbidity[1][:])*z, avg_target_values, 'o-', label='Average measured target amplitude', color='red')

s_legend = 12
s_axis = 14
s_title = 18
plt.title('ToF Amplitude Experiment Results', **csfont)
plt.xlabel(r'Attenuation Lengths [AL]', **hfont)
plt.ylabel('Amplitude $P_{target}$ [LSB]',)
plt.grid(True)
plt.legend(prop={'size': s_legend})
plt.show()
#plt.rcParams["figure.figsize"] = (9,7)

