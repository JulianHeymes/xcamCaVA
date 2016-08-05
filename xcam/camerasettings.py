import numpy as np


class CameraSettings:
    def __init__(self):
        self.voltages = []
        self.parameters = []
        self.timeout = 0
        self.timeunits = 'ms'
        self.sequencefile = ''
        self.parameterfile = ''
        self.voltagefile = ''
        self.frametype = ''
        self.columns = 0
        self.rows = 0
        self.integrationtime = 0
        self.cdsgain = 0
        self.cdsoffset = 0

    def read_parameter_file(self, fn):
        self.parameterfile = fn
        self.parameters = np.loadtxt(fn, delimiter=',')

    def read_voltage_file(self, fn):
        self.voltagefile = fn
        self.voltages = np.loadtxt(fn, delimiter=',')

    def get_settings(self):
        settings = {}
        settings['voltages'] = self.voltages
        settings['parameters'] = self.parameters
        settings['timeout'] = self.timeout
        settings['timeunits'] = self.timeunits
        settings['sequencerfile'] = self.sequencerfile
        settings['parameterfile'] = self.parameterfile
        settings['voltagefile'] = self.voltagefile
        settings['frametype'] = self.frametype
        settings['columns'] = self.columns
        settings['rows'] = self.rows
        settings['integrationtime'] = self.integrationtime
        settings['cdsgain'] = self.cdsgain
        settings['cdsoffset'] = self.cdsoffset
        return settings

    def convert_frametype(self):
        if self.frametype == 'FT':
            return 0
        elif self.frametype == 'FF':
            return 1
        
    def convert_time(self):
        if self.timeunits == 'ms':
            return 0
        elif self.timeunits == '1/100s':
            return 1
        elif self.timeunits == 's':
            return 2

    
        
        
