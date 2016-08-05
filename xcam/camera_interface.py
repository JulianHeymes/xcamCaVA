import camera
import camera_settings as cs
import numpy as np
## hard coded number of params and voltages
nparams = 72
nvoltages = 12


class CameraInterface:
    def __init__(self):
        self.camera = camera.Camera()

    def initialise(self):
        self.camera.setup()
        print self.camera.set_CCD_on()
        self.camera.frame_grab_setup_sn(self.settings.columns,
                                        self.settings.rows,
                                        0,
                                        0,
                                        self.settings.columns,
                                        self.settings.rows,
                                        1)

    def get_parameters(self):
        params = [self.camera.get_single_param(i)[1] for i in range(nparams)]
        return params

    def get_voltages(self):
        voltages = [self.camera.get_voltage(i)[1] for i in range(nvoltages)]
        return voltages
        
    def get_image(self):
        return self.camera.grab_frame(self.settings.rows, self.settings.columns)

    def process_buffer(self, img):
        img = np.asarray(img)
        img = img.reshape(self.settings.rows, self.settings.columns, order='F')
        return img

    def update_settings(self, settings):
        self.settings = settings
        self.apply_settings()

    def apply_settings(self):
        #go through current settings and update the camera
        #get the settings dictionary
        sets = self.settings.get_settings()
        for key in sets:
            if type(sets[key]) is list:
                self.set_param_list(key, sets[key])
            else:
                self.set_single_param(key, sets[key])
        #cds
        self.camera.set_cds_gain(self.settings.cdsgain)
        self.camera.set_cds_offset(self.settings.cdsoffset)
        self.initialise()

    def set_single_param(self, key, value):
        if key in cs.paramslist:
            paramid = cs.paramslist[key]
            print paramid, value
            print self.camera.set_single_param(paramid, value)
        if key in cs.voltslist:
            voltid = cs.voltslist[key]
            self.camera.set_voltage(voltid, value)

    def set_param_list(self, key, value):
        if key == "parameters":
            for i,val in enumerate(value):
                self.camera.set_single_param(i, val)
        elif key == "voltages":
            for i,val in enumerate(value):
                self.camera.set_voltage(i, val)

    def set_voltage(self, key, value):
        self.camera.set_voltage(cs.voltslist[key], int(value))

    def set_param(self, key, value):
        self.camera.set_single_param(cs.paramslist[key], int(value))
    
