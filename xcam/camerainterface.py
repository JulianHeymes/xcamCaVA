import camera
import camerasettings as cs
import numpy as np
## hard coded number of params and voltages
nparams = 72
nvoltages = 12

paramslist = {'rows': 11, 'columns': 10, 'frametype': 8,
              'integrationtime': 15, 'timeunits': 64,
              'parallelbinning': 9}
voltslist = {'image': 0, 'store': 1, 'serial': 2, 'reset': 3,
             'vod': 4, 'vrd': 5, 'vdd': 6, 'vog': 7, 'vss' 9,
             'spr': 10, 'emv': 11}

class CameraInterface:
    def __init__(self, camera):
        self.camera = camera
        self.settings = cs.CameraSettings()

    def get_parameters(self):
        params = [self.camera.get_single_param(i)[1] for i in range(nparams)]
        return params

    def get_voltages(self):
        voltages = [self.camera.get_voltage(i)[1] for i in range(nvoltages)]
        return voltages
        
    def get_image(self):
        return self.camera.grab_frame(528, 552)[1]

    def process_buffer(self, img):
        img = np.asarray(img)
        img = img.reshape(528, 552, order='F')
        return img

    def update_settings(self, settings):
        self.settings = settings
        self.apply_settings()

    def apply_settings(self):
        #go through current settings and update the camera
        self.read_parameter_file
        camera.set_single_param
