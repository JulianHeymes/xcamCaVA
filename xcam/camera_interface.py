import camera
import camera_settings as cs
import numpy as np
import time
## hard coded number of params and voltages
nparams = 72
nvoltages = 12


class CameraInterface:
    def __init__(self):
        self.camera = camera.Camera()

    def get_parameters(self):
        params = [self.camera.get_single_param(i)[1] for i in range(nparams)]
        return params

    def get_voltages(self):
        voltages = [self.camera.get_voltage(i)[1] for i in range(nvoltages)]
        return voltages
        
    def get_image(self):
        (err,image) = self.camera.grab_frame(self.settings.columns, self.settings.rows)
        time.sleep(0.05)
        return (err,image)

    def process_buffer(self, img):
        img = np.asarray(img)
        img = img.reshape(self.settings.rows, self.settings.columns, order='F')
        return img

    def update_settings(self, settings):
        self.settings = settings
        self.apply_settings()

    def setup_camera(self):
        sets = self.settings.get_settings()
        self.camera.setup(sets['sequencerfile'])
        for key in sets:
            if type(sets[key]) is list:
                self.set_param_list(key, sets[key])
            else:
                self.set_single_param(key, sets[key])
        self.setup_single_node()

    def clear(self):
        self.camera.set_CCD_on()
        #set a short integration time to reduce lag
        self.set_parameter('integrationtime', 1)
        self.get_image()
        #reset the integration time to user specified level
        self.set_parameter('integrationtime', self.settings.integrationtime)
                
    def setup_single_node(self):
        self.camera.frame_grab_setup_sn(self.settings.columns,
                                        self.settings.rows,
                                        0,
                                        0,
                                        self.settings.columns,
                                        self.settings.rows,
                                        1)
        
    def apply_settings(self):
        #go through current settings and update the camera
        #get the settings dictionary
        sets = self.settings.get_settings()
        self.setup_camera()
        for key in sets:
            if type(sets[key]) is list:
                self.set_param_list(key, sets[key])
        for key in sets:
            if type(sets[key]) is not list:
                self.set_single_param(key, sets[key])

        #cds
        self.camera.set_cds_gain(self.settings.cdsgain)
        self.camera.set_cds_offset(self.settings.cdsoffset)
        self.clear()

    def set_single_param(self, key, value):
        if key in cs.paramslist:
            paramid = cs.paramslist[key]
            self.camera.set_single_param(paramid, int(value))
        elif key in cs.voltslist:
            voltid = cs.voltslist[key]
            self.camera.set_voltage(voltid, int(value))

    def set_param_list(self, key, value):
        if key == "parameters":
            for i,val in enumerate(value):
                self.camera.set_single_param(i, int(val))
        elif key == "voltages":
            for i,val in enumerate(value):
                self.camera.set_voltage(i, int(val))

    def set_voltage(self, key, value):
        return self.camera.set_voltage(cs.voltslist[key], int(value))

    def set_parameter(self, key, value):
        return self.camera.set_single_param(cs.paramslist[key], int(value))
    
