import ctypes
import numpy as np
import time
from types import *

errorlist = ["No Error", "Interface Serial Number Not found.", "Interface not initialised",
             "Array too large", "Interface communication failed.", "Error code array contains errors",
             "Transaction timed out.", "File not found", "Error in argument value", "Memory allocation failure",
             "Number of nodes not supported", "CDS Type is Unknown.", "Null buffer argument passed",
             "Comms protocol returned NAK"]


class CameraSettings:
    def __init__(self):
        self.voltages = [0,0,0,0]
        self.parameters = [0,0,0,0]
        
class Camera:
    def __init__(self):
        self.settings = CameraSettings()
        self.lib = ctypes.WinDLL('xcmclm.dll') #doesn't work on linux, duh
        #discover the camera system
        self.error, self.serial = self.discover()
        if self.error != 0:
            print translate_error(self.error)
        self.error = self.initialize()
        if self.error !=0:
            print translate_error(self.error)
        self.start_production_image(0)
        time.sleep(0.1)
        print self.send_pulse(0, 50, 50)
        time.sleep(0.5)
        print self.initialise_spi_bus()
        time.sleep(0.1)
        print self.frame_grab_setup_sn(552, 528, 0, 0, 552, 528, 1)[1]
        
        
    def translate_error(selfec):
        return errorlist[ec]
    

    def to_ctype_int_array(self, pyarr):
        return (ctypes.c_int * len(pyarr))(*pyarr)

    def get_version(self):
        xcmVer = ctypes.WINFUNCTYPE(ctypes.c_int,
                                ctypes.c_char_p)
        xcamDllApiParams = (1,"p1", 0),
        version = xcmVer(("xcm_clm_dll_version", self.lib), xcamDllApiParams)
        p1 = ctypes.c_char_p("")
        err = version(p1)
        return (err, p1.value)

    def discover(self):
        xcmDiscover = ctypes.WINFUNCTYPE(ctypes.c_int,
                                     ctypes.c_void_p,
                                     ctypes.c_int,
                                     ctypes.c_void_p)
        params = (1, "devices", 0), (1, "num_devices", 0), (1, "num_found", 0)
        disc = xcmDiscover(("xcm_clm_discover", self.lib), params)
        devices = ctypes.c_void_p(1)
        num_devices = ctypes.c_int(1)
        num_found = ctypes.c_void_p(1)
        err = disc(ctypes.byref(devices), num_devices, ctypes.byref(num_found))
        return (err, devices.value)

    def initialize(self):
        xcmInit = ctypes.WINFUNCTYPE(ctypes.c_int,
                                     ctypes.c_void_p,
                                     ctypes.c_void_p,
                                     ctypes.c_int,
                                     ctypes.c_void_p)
        params = (1, "serials", 0), (1, "errorcodes", 0), (1, "numserials", 0), (1, "numfound", 0)
        numserials = ctypes.c_int(1)
        serials = ctypes.c_int(self.serial)
        errcodes = ctypes.c_int(0)
        num_found = ctypes.c_int(0)
        init = xcmInit(("xcm_clm_init", self.lib), params)
        err = init(ctypes.byref(serials), ctypes.byref(errcodes), numserials, ctypes.byref(num_found))
        return err

    def get_sw_version(self):
        xcm_sw_ver = ctypes.WINFUNCTYPE(ctypes.c_int,
                                        ctypes.c_int,
                                        ctypes.c_char_p)
        params = (1, "srl", 0), (1, "bffr", 0)
        sw_ver = xcm_sw_ver(("xcm_clm_ifsver", self.lib), params)
        srl = ctypes.c_int(self.serial)
        bffr = ctypes.create_string_buffer(26)   
        err = sw_ver(srl, bffr)
        return (err,bffr.value)
    
    def get_hw_version(self):
        xcm_hw_ver = ctypes.WINFUNCTYPE(ctypes.c_int,
                                        ctypes.c_int,
                                        ctypes.c_char_p)
        params = (1, "srl", 0), (1, "bffr", 0)
        hw_ver = xcm_hw_ver(("xcm_clm_fpgaver", self.lib), params)
        srl = ctypes.c_int(self.serial)
        bffr = ctypes.create_string_buffer(256)   
        err = hw_ver(srl, bffr)
        return (err,bffr.value)

    def set_CDS_gain(self, gain):
        srl = ctypes.c_int(self.serial)
        gain = ctypes.c_short(gain)
        xcm_cds_off = ctypes.WINFUNCTYPE(ctypes.c_int,
                                         ctypes.c_int,
                                         ctypes.c_short)
        params = (1, "srl", 0), (1, "gain", 0)
        cds_o = xcm_cds_off(("xcm_clm_cds_gain", self.lib), params)
        return cds_o(srl, gain)

    def set_CDS_offset(self, offset):
        srl = ctypes.c_int(self.serial)
        offset = ctypes.c_short(offset)
        xcm_cds_off = ctypes.WINFUNCTYPE(ctypes.c_int,
                                         ctypes.c_int,
                                         ctypes.c_short)
        params = (1, "srl", 0), (1, "offset", 0)
        cds_o = xcm_cds_off(("xcm_clm_cds_offset", self.lib), params)
        return cds_o(srl, offset)

    def set_CCD_on(self):
        srl = ctypes.c_int(self.serial)
        on = ctypes.c_short(1)
        ccd_on = ctypes.WINFUNCTYPE(ctypes.c_int,
                                    ctypes.c_int,
                                    ctypes.c_short)
        params = (1, "srl", 0), (1, "on", 0)
        ccd_pow = ccd_on(("xcm_clm_ccd_power", self.lib), params)
        return ccd_pow(srl, on)

    def set_CCD_off(self):
        srl = ctypes.c_int(srl)
        off = ctypes.c_short(0)
        ccd_on = ctypes.WINFUNCTYPE(ctypes.c_int,
                                    ctypes.c_int,
                                    ctypes.c_short)
        params = (1, "srl", 0), (1, "off", 0)
        ccd_pow = ccd_on(("xcm_clm_ccd_power", self.lib), params)
        return ccd_pow(srl, off)

    def send_echo_request(self):
        srl = ctypes.c_int(self.serial)
        message = ctypes.create_string_buffer(20)
        ech_req = ctypes.WINFUNCTYPE(ctypes.c_int,
                                     ctypes.c_int,
                                     ctypes.c_char_p)
        params = (1, "srl", 0), (1, "msg", 0)
        ereq = ech_req(("xcm_clm_echoreq", self.lib), params)
        err = ereq(srl, message)
        return (err, message)

    def set_voltage(self, index, value):
        srl = ctypes.c_int(self.serial)
        index = ctypes.c_short(index)
        value = ctypes.c_void_p(value)
        sv = ctypes.WINFUNCTYPE(ctypes.c_int,
                                ctypes.c_int,
                                ctypes.c_short,
                                ctypes.c_void_p)
        params = (1, "srl", 0), (1, "vindex", 0), (1, "value", 0)
        set_v = sv(("xcm_clm_set_voltage", self.lib), params)
        return set_v(srl, index, value)

    def get_voltage(self, index):
        srl = ctypes.c_int(self.serial)
        index = ctypes.c_short(index)
        value = ctypes.c_void_p(1)
        sv = ctypes.WINFUNCTYPE(ctypes.c_int,
                                ctypes.c_int,
                                ctypes.c_short,
                                ctypes.c_void_p)
        params = (1, "srl", 0), (1, "vindex", 0), (1, "value", 0)
        set_v = sv(("xcm_clm_get_voltage", self.lib), params)
        err = set_v(srl, index, ctypes.byref(value))
        return (err, value.value)
    
    def load_sequencer(self, filename):
        seq_file = ctypes.create_string_buffer(filename)
        srl = ctypes.c_int(self.serial)
        ls = ctypes.WINFUNCTYPE(ctypes.c_int,
                                ctypes.c_int,
                                ctypes.c_char_p)
        params = (1, "srl", 0), (1, "seqfile", 0)
        load_s = ls(("xcm_clm_load_seq", self.lib), params)
        err = load_s(srl, seq_file)
        return err 

    def read_single_sequencer_command(self, i):
        srl = ctypes.c_int(self.serial)
        index = ctypes.c_short
        value = ctypes.c_void_p(0)
        rssc = ctypes.WINFUNCTYPE(ctypes.c_int,
                                  ctypes.c_int,
                                  ctypes.c_short,
                                  ctypes.c_void_p)
        params = (1, "srl", 0), (1, "index", 0), (1, "value", 0)
        re = rssc(("xcm_clm_read_seq", self.lib), params)
        err = re(srl, i, ctypes.byref(value))
        return value.value

    def set_single_param(self, index, value):
        srl = ctypes.c_int(self.serial)
        index = ctypes.c_short(index)
        value = ctypes.c_short(value)
        sst = ctypes.WINFUNCTYPE(ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_short,
                                 ctypes.c_short)
        params = (1, "srl", 0), (1, "index", 0), (1, "value", 0)
        sst_c = sst(("xcm_clm_set_param", self.lib), params)
        return sst_c(srl, index, value)

    def get_single_param(self, index):
        srl = ctypes.c_int(self.serial)
        index = ctypes.c_short(index)
        value = ctypes.c_void_p(0)
        sst = ctypes.WINFUNCTYPE(ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_short,
                                 ctypes.c_void_p)
        params = (1, "srl", 0), (1, "index", 0), (1, "value", 0)
        sst_c = sst(("xcm_clm_get_param", self.lib), params)
        err = sst_c(srl, index, ctypes.byref(value))
        return (err, value.value)

    def write_byte_eeprom(self, address, value):
        srl = ctypes.c_int(self.serial)
        add = ctypes.c_int(address)
        value = ctypes.c_int(value)
        wbee = ctypes.WINFUNCTYPE(ctypes.c_int,
                                  ctypes.c_int,
                                  ctypes.c_int,
                                  ctypes.c_int)
        params = (1, "srl", 0), (1, "address", 0), (1, "value", 0)
        wbee_c = wbee(("xcm_clm_eepwrite", self.lib), params)
        return wbee_c(srl, add, value)

    def read_byte_eeprom(self, address):
        srl = ctypes.c_int(self.serial)
        add = ctypes.c_int(address)
        value = ctypes.c_void_p(0)
        rbee = ctypes.WINFUNCTYPE(ctypes.c_int,
                                  ctypes.c_int,
                                  ctypes.c_int,
                                  ctypes.c_void_p)
        params = (1, "srl", 0), (1, "address", 0), (1, "value", 0)
        rbee_c = rbee(("xcm_clm_eepread", self.lib), params)
        err = rbee_c(srl, add, ctypes.byref(value))
        return (err, value.value)

    def set_timeout_ms(self, timeout):
        srl = ctypes.c_int(self.serial)
        to = ctypes.c_long(timeout)
        stms = ctypes.WINFUNCTYPE(ctypes.c_int,
                                  ctypes.c_int,
                                  ctypes.c_long)
        params = (1, "srl", 0), (1, "timeout", 0)
        stms_c = stms(("xcm_clm_set_timeout", self.lib), params)
        return stms_c(srl, timeout)
    
    def reset_interface(self):
        srl = ctypes.c_int(self.serial)
        ri = ctypes.WINFUNCTYPE(ctypes.c_int,
                                ctypes.c_int)
        params = (1, "serial", 0)
        ri_c = ri(("xcm_clm_interface_reset", self.lib), params)
        return ri_c(srl)



    def frame_grab_setup(self, numcols, numrows, top, left, height, width):
        img_bffr = ctypes.create_string_buffer(0)
        fgs = ctypes.WINFUNCTYPE(ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_void_p)
        params = (1, "serial", 0), (1, "numcols", 0), (1, "numrows", 0), (1, "top", 0), (1, "left", 0), (1, "height", 0), (1, "width", 0), (1, "img", 0)
        fgs_c = fgs(("xcm_clm_grab_setup", self.lib), params)
        fgs_c(self.serial, numcols, numrows, top, left, height, width, img_bffr)
        return img_bffr

    def frame_grab_setup_sn(self, numcols, numrows, top, left, height, width, node):
        img_bffr = (ctypes.c_uint16*numcols*numrows)()
        fgs = ctypes.WINFUNCTYPE(ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_void_p,
                                 ctypes.c_int)
        params = (1, "serial", 0), (1, "numcols", 0), (1, "numrows", 0), (1, "top", 0), (1, "left", 0), (1, "height", 0), (1, "width", 0), (1, "img", 0), (1, "node", 0)
        fgs_c = fgs(("xcm_clm_grab_setup_1node", self.lib), params)
        err = fgs_c(self.serial, numcols, numrows, top, left, height, width, img_bffr, node)
        return (err, img_bffr)

    def frame_grab_setup_deint(self, numcols, numrows, top, left, height, width):
        img_bffr = (ctypes.c_uint16*numcols*numrows)()
        fgs = ctypes.WINFUNCTYPE(ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_void_p)
        params = (1, "serial", 0), (1, "numcols", 0), (1, "numrows", 0), (1, "top", 0), (1, "left", 0), (1, "height", 0), (1, "width", 0), (1, "img", 0)
        fgs_c = fgs(("xcm_clm_grab_setup_deint4", self.lib), params)
        err = fgs_c(self.serial, numcols, numrows, top, left, height, width, img_bffr)
        return (err, img_bffr)

    def set_overscan(self, overscan):
        so = ctypes.WINFUNCTYPE(ctypes.c_int,
                                ctypes.c_int)
        params = (1, "os", 0)
        so_c = so(("xcm_clm_set_overscan", self.lib), params)
        return so_c(overscan)

    def grab_frame(self, numcols, numrows):
        image = (ctypes.c_uint16*numcols*numrows)()
        gf = ctypes.WINFUNCTYPE(ctypes.c_int,
                                ctypes.c_int,
                                ctypes.c_void_p)
        params = (1, "serial", 0), (1, "image", 0)
        gf_c = gf(("xcm_clm_grab_pointer", self.lib), params)
        err = gf_c(self.serial, image)
        return (err, image)

    def close_session(self):
        cs = ctypes.WINFUNCTYPE(ctypes.c_int)
        cs_c = cs(("xcm_clm_terminate", self.lib))
        return cs_c()

    def cancel_frame_grab(self):
        cfg = ctypes.WINFUNCTYPE(ctypes.c_int,
                                 ctypes.c_int)
        params = (1, "serial", 0)
        cfg_c = cfg(("xcm_clm_cancel_grab", self.lib), params)
        return cfg_c(self.serial)

    def get_interface_status(self):
        status = ctypes.c_short
        gis = ctypes.WINFUNCTYPE(ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_void_p)
        params = (1, "serial", 0), (1, "status", 0)
        gis_c = gis(("xcm_clm_get_interface_status", self.lib), params)
        err = gis_c(self.serial, ctypes.byref(status))
        return (err, status.value)

    def get_camera_serial_number(self):
        val = ctypes.c_char_p("")
        gcsn = ctypes.WINFUNCTYPE(ctypes.c_int,
                                  ctypes.c_int,
                                  ctypes.c_char_p)
        params = (1, "serial", 0), (1, "value", 0)
        gcsn_c = gcsn(("xcm_clm_get_cam_serial_number", self.lib), params)
        err = gcsn_c(self.serial, val)
        return (err, val.value)

    def send_pulse(self, tline, delay, width):
        tline = ctypes.c_int(tline)
        delay = ctypes.c_uint(delay)
        width = ctypes.c_uint(width)
        sp = ctypes.WINFUNCTYPE(ctypes.c_int,
                                ctypes.c_int,
                                ctypes.c_int,
                                ctypes.c_uint,
                                ctypes.c_uint)
        params = (1, "serial", 0), (1, "tline", 0),(1, "delay", 0),(1, "width", 0)
        sp_c = sp(("xcm_clm_pulse", self.lib), params)
        return sp_c(self.serial, tline, delay, width)

    def get_timing_estimates(self, texposure, treadout, tbusy, tcycle, buffsz):
        gte = ctypes.WINFUNCTYPE(ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.POINTER(ctypes.c_int),
                                 ctypes.POINTER(ctypes.c_int),
                                 ctypes.POINTER(ctypes.c_int),
                                 ctypes.POINTER(ctypes.c_int))
        params = (1, "serial", 0), (1, "texposure", 0), (1, "treadout", 0), (1, "tbusy", 0), (1, "tcycle", 0), (1, "bffsize", 0)
        gte_c = gte(("xcm_clm_get_timings", self.lib), params)
        return gte_c(self.serial, texposure, treadout, tbusy, tcycle, buffsz)

    def read_fpga_sector(self, dest, sector):
        bffr = ctypes.c_char_p("")
        rfs = ctypes.WINFUNCTYPE(ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_char_p)
        params = (1, "serial", 0), (1, "dest", 0),(1, "sector", 0),(1, "bffr", 0)
        rfs_c = rfs(("xcm_clm_read_fpga_sector", self.lib), params)
        err = rfs_c(self.serial, dest, sector, bffr)
        return (err, bffr.value)

    def start_production_image(self, destfpga):
        spi = ctypes.WINFUNCTYPE(ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int)
        params = (1, "serial", 0), (1, "destfpga", 0)
        spi_c = spi(("xcm_clm_start_production_image", self.lib), params)
        return spi_c(self.serial, destfpga)

    def initialise_spi_bus(self):
        ipi = ctypes.WINFUNCTYPE(ctypes.c_int,
                                 ctypes.c_int)
        params = (1, "serial", 0),
        ipi_c = ipi(("xcm_clm_initialise_spi", self.lib), params)
        return ipi_c(self.serial)

    def get_fpga_status(self, destfpga):
        gfs = ctypes.WINFUNCTYPE(ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_int)
        params = (1, "serial", 0), (1, "destfpga", 0)
        gfs_c = gfs(("xcm_clm_get_fpga_status", self.lib), params)
        return gfs_c(self.serial, destfpga)

    def set_grab_speed(self, speed):
        sgs = ctypes.WINFUNCTYPE(ctypes.c_int,
                                 ctypes.c_int,
                                 ctypes.c_short)
        params = (1, "serial", 0), (1, "speed", 0)
        sgs_c = sgs(("xcm_clm_set_grab_speed", self.lib), params)
        return sgs_c(self.serial, speed)


camera = Camera()
print camera.serial




        
