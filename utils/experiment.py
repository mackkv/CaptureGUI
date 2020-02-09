# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 12:00:15 2020

@author: mackk
"""
import constant
import datetime
import base64

class Experiment:
    def __init__(self):
        self._title = ''
        self._location = {'Building' : [],
                          'Room Number' : [],
                          'Environment' : []}
        self._date_and_time = datetime.datetime
        self._description = {}
        self._parameters = {'turbidity' : [0,1,2,3,4,5],
                            'distance'  : [24],
                            'modulation': ['Sinusoidal'],
                            'frequency' : ['24 Mhz'],
                            'target'    : [0, 1],
                            'mode'      : ['grayscale', 'RGB', 'DCS']}
        self._equipment = {'CAMS'  : None,
                            'TRACK': None,
                            'TURB_CON' : None,
                            'TURB_SENSE': None}
        
        self._num_samples = None
        self._ui_events = False
        self._ui_msgs = {}
        self._dataset = {}
        self._save_dir = []
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        self._title = title
        
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, location):
        self._location = location
        
    @property
    def date_and_time(self):
        return self._date_and_time
    
    @date_and_time.setter
    def date_and_time(self, date_and_time):
        self._date_and_time = date_and_time
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        self._description = description
        
    @property
    def parameters(self):
        return self._parameters
    
    @parameters.setter
    def parameters(self, parameters):
        self._parameters = parameters
        
    @property
    def ui_events(self):
        return self._ui_events
    
    @ui_events.setter
    def ui_events(self, ui_events):
        self._ui_events = ui_events
        
    @property
    def ui_msgs(self):
        return self._ui_msgs
    
    @ui_msgs.setter
    def ui_msgs(self, ui_msgs):
        self._ui_msgs = ui_msgs
        
    @property
    def num_samples(self):
        return self._num_samples
    
    @num_samples.setter
    def num_samples(self, num_samples):
        self._num_samples = num_samples
        
    @property
    def equipment(self):
        return self._equipment
    
    @equipment.setter
    def equipment(self, equipment):
        self._equipment = equipment
        
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data):
        self._data = data
        
    def run(self):
        if self._num_samples is None:
            raise ValueError('Number of samples not set')
        if self._equipment['CAM'] is None:
            raise ValueError('No capture device selected')
        else:
            print('Cam connected, samples set')
            
