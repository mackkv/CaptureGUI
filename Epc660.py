# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 23:07:21 2019

@author: Labadmin
"""
import socket
import struct
import numpy as np
import cv2
import constant
import datetime
import base64
#import pcl

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
            
            
class EpcTcp:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_timeout = 2
        
    def set_timeout(self, timeout):
        self.socket_timeout = timeout
        
    def get_socket_timeout(self):
        return self.socket_timeout
    
    def get_socket(self):
        return self.sock
    
    def connect(self, tcp_ip, tcp_port):
        self.sock.connect((tcp_ip, tcp_port))
        
#    def init_socket(self):
#        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    
    def send_and_recv(self, command, buffer, parameters=""):
        #print(parameters)
        try:
            for param in [parameters]:
                command = command + " " + str(param)
            self.sock.sendall(bytes((command + '\n').encode("ascii")))
            # Look for the response
            data = []
            coded_data = []
#            print(command)
            while data != b'':
                data = self.sock.recv(buffer)
                
#                data.decode('ascii')
                coded_data.append(data)
                
#            print("PRINTING CODED DATA:" + "\n")
#            print(coded_data)
#            print(type(coded_data))
        finally:
            self.sock.close()
        
        return coded_data
    
    def decode_data2(self, coded_data, dtype):
        hex_data = []
        for data_msg in coded_data:
            hex_data.append(data_msg.decode("utf-16"))
        
        print("PRINTING DECODED DATA:" + "\n")
        print(hex_data)
        return hex_data
    
    def decode_data3(self, coded_data, dtype):
        hex_data = []
        for data_msg in coded_data:
#            hex_data.append(struct.unpack('hhl', data_msg))
        
            print("PRINTING DECODED DATA: " + "\n")
            print(data_msg)
        return hex_data
    
    def decode_data(self, coded_data, dtype):
        data_up = []
        for data_msg in coded_data:
            data_len = len(data_msg)
            for i in range(0, data_len, 2):
                p_up = struct.unpack("<h", data_msg[i:i+2])
                data_up.append(p_up)
        if dtype == "distance":
            decoded_data = np.reshape(np.array(data_up), (constant.CAM_RESX, constant.CAM_RESY))
        elif dtype == "distance_custom":
            decoded_data = self.compute_dist(data_up)
        elif dtype == "amplitude":
            decoded_data = self.compute_amplitude(data_up)
        elif dtype == "dcs":
            decoded_data = np.reshape(np.array(data_up), (4, constant.CAM_RESY, constant.CAM_RESX), order='C')
        elif dtype == "grayscale":
#            decoded_data = coded_data.decode("ascii")
            decoded_data = np.reshape(np.array(data_up), (4, constant.CAM_RESX, constant.CAM_RESY))
        elif dtype == "info":
            decoded_data = data_up
        else:
            print("E: No decode type specified, returning original coded data")
            decoded_data = coded_data
            
        return decoded_data
            
    def compute_amplitude(self, data):
        raw_max = np.max(data)
        image = (data/raw_max)*constant.MAX_PVALUE
        image = np.reshape(np.array(image), (constant.CAM_RESX,constant.CAM_RESY))
        return image
    
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

class EpcCam:
    def __init__(self):
        
        #self.epc_conn = EpcTcp()
        self.epc_conn = []
        self.tcp_ip = []
        self.tcp_port = []
        self.buffer_size = 2048
        self.device_address = self.get_dev_address
        self.integration_time = []
        self.mod_freq = []
        self.server_version = []
        self.ic_version = []
        self.part_version = []
        self.chip_info = []
    
    def get_dev_address(self):
        return self.device_address
    
    def get_offset(self):
        command = constant.CMD_GET_OFFSET
        coded_data = self.epc_conn.send_and_recv(command, buffer = self.buffer_size)
        offset = self.epc_conn.decode_data(coded_data, "info")
        return offset
    
    def load_config(self, config_filename):
        command = constant.CMD_LOAD_CONFIG
        self.setup_epctcp()
        coded_data = self.epc_conn.send_and_recv(command + config_filename, buffer = self.buffer_size)
        resp = self.epc_conn.decode_data(coded_data, "info")
        return resp
    
    def get_cam_temp(self):
        command = constant.CMD_GET_TEMPS
        self.setup_epctcp()
        coded_data = self.epc_conn.send_and_recv(command, buffer = self.buffer_size)
        temp_data = self.epc_conn.decode_data(coded_data, "info")
        return temp_data
        
    def get_tcp_ip(self):
        return self.tcp_ip
    
    def get_tcp_port(self):
        return self.tcp_port
    
    def get_buffer(self):
        return self.buffer_size
    
    def get_int_time(self):
        command = constant.CMD_GET_IMAGING_TIME
        self.setup_epctcp()
        coded_data = self.epc_conn.send_and_recv(command, buffer = self.buffer_size)
        self.integration_time = self.epc_conn.decode_data(coded_data, "info")# is getImagingTime actually the correct command for this?
        return self.integration_time
    
    def get_mod_freq(self):
        command = constant.CMD_GET_MOD_FREQ
        self.setup_epctcp()
        coded_data = self.epc_conn.send_and_recv(command, buffer = self.buffer_size)
        self.mod_freq = self.epc_conn.decode_data(coded_data,"info")
        return self.mod_freq
    
    def get_all_mod_freqs(self):
        command = constant.CMD_GET_ALL_MOD_FREQS
        self.setup_epctcp()
        coded_data = self.epc_conn.send_and_recv(command, self.buffer_size)
        decoded_data = self.epc_conn.decode_data(coded_data, "info")
        return decoded_data
    
    def get_server_version(self):
        command = constant.CMD_GET_SERVER_VER
        self.setup_epctcp()
        coded_data = self.epc_conn.send_and_recv(command, self.buffer_size)
        self.server_version = self.epc_conn.decode_data(coded_data, "info")
        return self.server_version
    
    def get_ic_version(self):
        command = constant.CMD_GET_IC_VER
        self.setup_epctcp()
        coded_data = self.epc_conn.send_and_recv(command, self.buffer_size)
        self.ic_version = self.epc_conn.decode_data(coded_data, "info")
        return self.ic_version
    
    def get_chip_info(self):
        command = constant.CMD_GET_CHIP_INFO
        self.setup_epctcp()
        coded_data = self.epc_conn.send_and_recv(command, self.buffer_size)
        self.chip_info = self.epc_conn.decode_data(coded_data, "info")
        return self.chip_info
    
    def get_part_version(self):
        command = constant.CMD_GET_PART_VER
        self.setup_epctcp()
        coded_data = self.epc_conn.send_and_recv(command, self.buffer_size)
        self.part_version = self.epc_conn.decode_data(coded_data, "info")
        return self.part_version
    
    def set_dev_address(self, address):
        self.device_address = address
        
    def set_buffer(self, buffer):
        self.buffer_size = buffer
        
    def set_tcp_ip(self, ip_address):
        self.tcp_ip = ip_address
        
    def set_tcp_port(self, port):
        self.tcp_port = port
        
    def set_roi(self, x1, x2, y1, y2):
        self.setup_epctcp()
        command = constant.CMD_SET_ROI
        coded_data = self.epc_conn.send_and_recv(command, buffer = self.buffer_size, parameters = [x1, x2, y1, y2])
        resp = self.epc_conn.decode_data(coded_data, "info")
        #print(resp)
        if resp == 1:
            print("ROI set successfully")
        else:
            print("E: ROI not set")
            
        return resp
        
    def set_modulation(self, mod):
        command = constant.CMD_SET_MOD_FREQ
        self.setup_epctcp()
        coded_data = self.epc_conn.send_and_recv(command, buffer = self.buffer_size, parameters = mod)
        decoded_data = self.epc_conn.decode_data(coded_data, "info")
        return decoded_data
    
    def select_mode(self, mode):
        command = constant.CMD_SELECT_MODE
        self.setup_epctcp()
        coded_data = self.epc_conn.send_and_recv(command, buffer = self.buffer_size, parameters = mode)
        decoded_data = self.epc_conn.decode_data(coded_data, "info")
        return decoded_data
        
    def set_int_time(self, t_int):
        command = "setIntegrationTime3D"
        self.integration_time = t_int
        self.setup_epctcp()
        coded_data = self.epc_conn.send_and_recv(command, buffer = self.buffer_size, parameters = t_int)
        decoded_data = self.epc_conn.decode_data(coded_data, "info")
        return decoded_data
    
    def load_xml_config(self, filename):
        command = constant.CMD_LOAD_CONFIG
        self.setup_epctcp()
        coded_data = self.epc_conn.send_and_recv(command, buffer = self.buffer_size, parameters = filename)
        decoded_data = self.epc_conn.decode_data(coded_data, "info")
        return decoded_data
        
    def setup_epctcp(self):
        self.epc_conn = EpcTcp()
        self.epc_conn.connect(self.tcp_ip, self.tcp_port)
    
#    def start_video(self, vtype):
        # TO DO 
#        
#    def stop_video(self):
#        # TO DO
        
    def take_image(self, itype):
        self.epc_conn = EpcTcp()
        self.epc_conn.connect(self.tcp_ip, self.tcp_port)
        if itype == "distance":
            command = "getDistanceSorted"
        elif itype == "amplitude":
            command = "getAmplitudeSorted"
        elif itype == "dcs":
            command = "getDCSSorted"
        elif itype == "grayscale":
            command = "getBWSorted"
        else:
            print("E: Image Type Not Recognized")

        coded_data = self.epc_conn.send_and_recv(command, buffer = self.buffer_size)
        decoded_data = self.epc_conn.decode_data(coded_data,itype)
        return decoded_data
    
    def take_video(self, itype, duration=1000):
        self.epc_conn = EpcTcp()
        self.epc_conn.connect(self.tcp_ip, self.tcp_port)
        
#        if itype == "distance":
#            command = "getDistanceSorted"
#        elif itype == "amplitude":
#            command = "getAmplitudeSorted"
#        elif itype == "dcs":
#            command = "getDCSSorted"
#        elif itype == "grayscale":
#            command = "getBWSorted"
#        else:
#            print("E: Image Type Not Recognized")
        command = 'startVideo'
        coded_data = self.epc_conn.send_and_recv(command, buffer = self.buffer_size)
        decoded_data = self.epc_conn.decode_data(coded_data, itype)
        return decoded_data
    
    def rotate_image(self, img, deg):
        # rotate image 
        n = (deg/90)
        img = np.rot90(np.uint8(img), k=n, axes=(1,0))
        return img

    def flip_image(self, img):
        return np.flip(img,1)
    
    def remove_lens_distortion(self, img):
        corrected_img = []
        return corrected_img
        
    def save_image(self, img, iname):
        cv2.imwrite(iname + '.png',img)
    
    def view_pointcloud(self, dist_data):
        pointcloud = []
    
if __name__ == "__main__":    
    TCP_IP = '192.168.7.2'
    TCP_PORT = 50660
    TCP_BUFFER = 8192
    TIMEOUT = 5
    
    cam = EpcCam()
    
    cam.set_buffer(TCP_BUFFER)
    cam.set_tcp_port(TCP_PORT)
    cam.set_tcp_ip(TCP_IP)
    
    
    part_ver = cam.get_part_version()
    server_ver = cam.get_server_version()
    ic_ver = cam.get_ic_version()
    chip_info = cam.get_chip_info()
#    mod_set = cam.set_modulation(750)
#    int_set = cam.set_int_time(1500)
#    int_time = cam.get_int_time()
    int_set = cam.set_int_time(4000)
    
    mod_freqs = cam.get_all_mod_freqs()
#    mod_freq = cam.get_mod_freq()
    mod_set =  cam.set_modulation(2)
#    int_set = cam.set_int_time(50)
#    cam.set_roi(50, 150, 50, 150)
#    cam.epc_conn.connect()
    num_frames = 10
    itype = "distance"
    config_filename = " /config/epc660_settings_default.xml"
    config_filename = " 1"
    ver = cam.get_ic_version()
    config_set = cam.load_config(config_filename)
    mode_set = cam.select_mode(0)
#    #img = np.zeros((num_frames,240,320))
#    for cap in range(num_frames):
#        img = cam.take_image(itype)
#        img = cam.rotate_image(img, 180)
#        img = cam.flip_image(img)
#        cv2.imshow(itype, img)
##        img = cv2.applyColorMap(np.uint8(img), cv2.COLORMAP_RAINBOW)
##        cv2.imshow(itype + " image", np.uint8(img))
##        int_time1 = cam.get_int_time()
#        cv2.waitKey(1)