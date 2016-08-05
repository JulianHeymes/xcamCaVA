import numpy as np

paramslist = {'rows': 11, 'columns': 10, 'frametype': 8,
              'integrationtime': 15, 'timeunits': 64,
              'parallelbinning': 9}
voltslist = {'image': 0, 'store': 1, 'serial': 2, 'reset': 3,
             'vod': 4, 'vrd': 5, 'vdd': 6, 'vog': 7, 'vss': 9,
             'spr': 10, 'emv': 11}

class CameraSettings:
    def __init__(self):
        self.voltages = []
        self.parameters = []
        self.timeout = 0
        self.timeunits = 'ms'
        self.sequencerfile = ''
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
        self.parameters = np.loadtxt(fn)
        self.parameters = [int(p) for p in self.parameters]

    def read_voltage_file(self, fn):
        self.voltagefile = fn
        self.voltages = np.loadtxt(fn)
        self.voltages = [int(v) for v in self.voltages]

    def get_settings(self):
        settings = {}
        settings['voltages'] = self.voltages
        settings['parameters'] = self.parameters
        settings['timeout'] = self.timeout
        settings['timeunits'] = self.convert_time()
        settings['Ttimeunits'] = self.timeunits
        settings['sequencerfile'] = self.sequencerfile
        settings['parameterfile'] = self.parameterfile
        settings['voltagefile'] = self.voltagefile
        settings['frametype'] = self.convert_frametype()
        settings['Tframetype'] = self.frametype
        settings['columns'] = self.columns
        settings['rows'] = self.rows
        settings['integrationtime'] = self.integrationtime
        settings['cdsgain'] = self.cdsgain
        settings['cdsoffset'] = self.cdsoffset
        return settings

    def convert_frametype(self):
        if self.frametype == 'FT':
            return 1
        elif self.frametype == 'FF':
            return 0
        
    def convert_time(self):
        if self.timeunits == 'ms':
            return 0
        elif self.timeunits == '1/100s':
            return 1
        elif self.timeunits == 's':
            return 2

    def set_voltage(self, key, value):
        vid = voltslist[key]
        self.voltages[vid] = value
        
    def set_param(self, key, value):
        pid = paramslist[key]
        self.parameters[pid] = value
        
        
        
