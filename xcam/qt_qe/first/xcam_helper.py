import xcam as xcm
import math
import numpy as np
import datetime
import h5py
import time
import struct
import binascii
import functools
import matplotlib.pyplot as plt
import ctypes
#first thing, grab serial number
s = 0
nc = 0
nr = 0

def get_settings():
    settings = {}
    settings['voltages'] = get_voltages()
    settings['params'] = get_params()
    settings['columns'] = nc
    settings['rows'] = nr
    settings['integrationTime'] = get_param(15)
    settings['parallelBinning'] = get_param(9)
    settings['frameType'] = get_frame_type()
    settings['EMV'] = get_EMV()
    return settings
             

def get_voltages():
    return [get_voltage(i) for i in range(12)]

def get_params():
    return [get_param(i) for i in range(72)]

def get_param(i):
    rv = xcm.get_single_param(s, i)[1]
    return rv

def get_voltage(i):
    rv = xcm.get_voltage(s, i)[1]
    return rv

def set_grab_speed(speed):
    return xcm.set_grab_speed(s, speed)

def load_sequencer_from_file(filename):
    return xcm.load_sequencer(s, filename)

def voltage_from_file(filename):
    v_vals = np.loadtxt(filename)
    regs = np.arange(len(v_vals))
    v_vals = [int(i) for i in v_vals]
    #zero
    [xcm.set_voltage(s, i, 0) for i in regs]
    [xcm.set_voltage(s, i, v_vals[i]) for i in regs]

def param_from_file(filename):
    p_vals = np.loadtxt(filename)
    regs = np.arange(len(p_vals))
    p_vals = [int(i) for i in p_vals]
    [xcm.set_single_param(s, i, 0) for i in regs]
    [xcm.set_single_param(s, i, p_vals[i]) for i in regs]

def print_all_params():
    regs = np.arange(72)
    print [xcm.get_single_param(s, i)[1] for i in regs]
    
def print_all_voltages():
    regs = np.arange(12)
    print [xcm.get_voltage(s, i)[1] for i in regs]
    
def set_numcols(nct):
    global nc
    nc = nct
    xcm.set_single_param(s, 10, nc)
    setup_single_node()

def set_numrows(ncr):
    global nr
    nr = ncr
    xcm.set_single_param(s, 11, nc)
    setup_single_node()

def set_frame_type(t):
    xcm.set_single_param(s, 8, t)

def get_frame_type():
    ft = xcm.get_single_param(s, 8)
    ft = get_param(8)
    return convert_frameType(ft)

def set_integration_time(t):
    xcm.set_single_param(s, 15, t)

def get_integration_time():
    return get_param(15)

def set_integration_tmode(t):
    xcm.set_single_param(s, 64, t)

def set_timeout(t):
    xcm.set_timeout_ms(s, t)
    
def set_cds_gain(gain):
    return xcm.set_CDS_gain(s, gain)

def set_cds_offset(offset):
    return xcm.set_CDS_offset(s, offset)

def set_parallel_binning(bin_sz):
    xcm.set_single_param(s, 9, bin_sz)

def set_imagev(v):
    xcm.set_voltage(s, 0, v)

def get_imagev():
    return xcm.get_voltage(s, 0)[1]

def set_storev(v):
    xcm.set_voltage(s, 1, v)

def get_storev():
    return xcm.get_voltage(s, 1)[1]

def set_serialv(v):
    xcm.set_voltage(s, 2, v)

def get_serialv(v):
    return returnxcm.get_voltage(s, 2)[1]

def set_resetv(v):
    xcm.set_voltage(s, 3, v)

def get_resetv(v):
    return xcm.get_voltage(s, 3)[1]
    
def set_vod(v):
    xcm.set_voltage(s, 4, v)

def get_vod():
    return xcm.get_voltage(s, 4)[1]

def set_vrd(v):
    xcm.set_voltage(s, 5, v)

def get_vrd():
    return xcm.get_voltage(s, 5)[1]

def set_vdd(v):
    xcm.set_voltage(s, 6, v)

def get_vdd():
    return xcm.get_voltage(s, 6)[1]

def set_vog(v):
    xcm.set_voltage(s, 7, v)

def get_vod():
    return xcm.get_voltage(s, 7)[1]
    
def set_vss(v):
    xcm.set_voltage(s, 9, v)

def get_vss():
    return xcm.get_voltage(s, 9)[1]
    
def set_vspr(v):
    xcm.set_voltage(s, 10, v)

def get_vspr():
    return xcm.get_voltage(s, 10)[1]

def set_EMV(v):
    if(v > 210):
        print "EMV set too high at ", v
        print "Setting to 210 and continuing"
        xcm.set_voltage(s, 11, 210)
    else:
        xcm.set_voltage(s, 11, v)

def get_EMV():
    return xcm.get_voltage(s, 11)[1]

def setup_single_node():
    xcm.frame_grab_setup_sn(s, nc, nr, 0, 0, nc, nr, 1)

def setup_single_node_window(startc, startr, wx, wy):
    xcm.frame_grab_setup_sn(s, nc, nr, startc, startr, wx, wy, 1)

def setup_single_row():
    xcm.frame_grab_setup_sn(s, nc, nr, 0, 0, nc, 1, 1)

def grab_single_row():
    set_numrows(1)
    setup_single_row()
    (err, image) = xcm.grab_frame(s, nc, 1)
    return image


def grab_window(wx, wy):
    (err, image) = xcm.grab_frame(s, wx, wy)
    time.sleep(0.1)
    if(err == 0):
        return image
    else:
        return xcm.translate_error(err)
    
def grab_single_node():
    (err, image) = xcm.grab_frame(s, nc, nr)
    time.sleep(0.05)
    if(err == 0):
        return image
    else:
        return xcm.translate_error(err)

    
def clear_image():
    grab_single_node()

def ccd_off():
    xcm.set_CCD_off(s)

def ccd_on():
    xcm.set_CCD_on(s)

def close():
    xcm.close_session()

def convert_time(time, unit):
    if(unit == "ms"):
        set_integration_tmode(0)
        return time
    elif(unit == "s"):
        set_integration_tmode(1)
        return time*100
    elif(unit == "1/100s"):
        set_integration_tmode(1)
        return time
    elif(unit == "1/10s"):
        set_integration_tmode(1)
        return time*10

def convert_frameType(ft):
    if(ft == 1):
        return "FT"
    elif(ft == 0 or ft == None):
        return "FF"
    elif(ft.lower() == "ft"):
        return 1
    elif(ft.lower() == "ff"):
        return 0

def initialize():
    global s
    s = xcm.discover()[1]
    xcm.initialize(s)
    xcm.start_production_image(s, 0)
    time.sleep(0.5)
    xcm.send_pulse(s, 0, 50, 50)
    time.sleep(2)
    xcm.initialise_spi_bus(s)
    time.sleep(0.2)
    setup_single_node()


def apply_settings(settings):
    param_from_file(settings['parameterFile'])
    time.sleep(0.1)
    voltage_from_file(settings['voltageFile'])
    time.sleep(0.1)
    set_frame_type(convert_frameType(settings['frameType']))
    set_numcols(settings['columns'])
    set_numrows(settings['rows'])
    set_integration_time(convert_time(settings['integrationTime'], settings['timeUnits']))
    set_timeout(convert_time(settings['timeout'], settings['timeUnits']))
    set_cds_gain(settings['CDSgain'])
    set_cds_offset(settings['CDSoffset'])
    set_timeout(convert_time(settings['timeout'], settings['timeUnits']))
    set_integration_time(convert_time(settings['integrationTime'], settings['timeUnits']))
    
def setup_camera(settings):
    global s
    s = xcm.discover()[1]
    print s
    print xcm.initialize(s)
    print xcm.start_production_image(s, 0)
    time.sleep(0.5)
    set_timeout(convert_time(settings['timeout'], settings['timeUnits']))
    xcm.send_pulse(s, 0, 50, 50)
    load_sequencer_from_file(settings['sequencerFile'])
    time.sleep(2)
    print xcm.initialise_spi_bus(s)
    time.sleep(0.2)
    param_from_file(settings['parameterFile'])
    time.sleep(0.1)
    voltage_from_file(settings['voltageFile'])
    time.sleep(0.1)
    set_frame_type(convert_frameType(settings['frameType']))
    set_numcols(settings['columns'])
    set_numrows(settings['rows'])
    set_integration_time(convert_time(settings['integrationTime'], settings['timeUnits']))
    set_timeout(convert_time(settings['timeout'], settings['timeUnits']))
    set_cds_gain(settings['CDSgain'])
    set_cds_offset(settings['CDSoffset'])
    set_timeout(convert_time(settings['timeout'], settings['timeUnits']))
    set_integration_time(convert_time(settings['integrationTime'], settings['timeUnits']))
    setup_single_node()

def get_timing_estimates():
    texposure = ctypes.c_int(get_integration_time())
    treadout = ctypes.c_int(0)
    tbusy = ctypes.c_int(0)
    tcycle = ctypes.c_int(0)
    buffsz = ctypes.c_int(nc*nr)
    xcm.get_timing_estimates(s, texposure,
                             treadout,
                             tbusy,
                             tcycle,
                             buffsz)
    return (treadout, tbusy, tcycle, buffsz)


def clear_ccd():
    ccd_on()
    set_integration_time(1)
    grab_single_node()
    grab_single_node()


def get_frame():
    img = grab_single_node()
    return img

def gsn_with_count(x):
    return grab_single_node()

def get_frames(n):
    imgs = [np.asarray(gsn_with_count(x)) for x in range(n)]
    return np.asarray(imgs)

def get_diff_frame():
    img1 = grab_single_node()
    img2 = grab_single_node()
    return (img2,img1)

def get_diff_frames(n):
    return [(grab_single_node(), grab_single_node()) for x in range(n)]

def process_buffer(img):
    img = np.asarray(img)
    img = img.reshape(nr, nc, order='F')
    return img

def process_windowed_buffer(img, wx, wy):
    img = np.asarray(img)
    img = img.reshape(wx, wy, order='F')
    return img

def test_image(settings):
    setup_camera(settings)
    clear_ccd()
    img = get_frame()
    img = np.frombuffer(img, dtype=np.ushort)
    img = np.reshape(img, (nr,nc))
    plt.imshow(img)
    plt.show()
    

def convert_val(val):
    if(val == None):
        return 0
    elif(type(val) == list):
        return [convert_val(v) for v in val]
    else:
        return val

def save_settings(dset, datt):
    for key, val in datt.items():
        dset.attrs.create(key, convert_val(val))

def continuous_readout(t):
    t0 = time.time()
    te = t0
    dn_count = 0
    while(te - t0 < t):
        im = get_frame()
        im = process_buffer(im)
        dn_count += np.sum(im)
        te = time.time()
    return dn_count

def grab_XRCAL(fn, group_n):
    dn_count = 0
    num_stacks = 10
    img_per_stack = 50
    settings = {}
    f = h5py.File(fn, 'a')
    grp = f.create_group(group_n)
    set_EMV(0)
    settings.update(get_settings())
    clear_ccd()
    for i in np.arange(num_stacks):
        dset = grp.create_dataset(str(i), (img_per_stack, settings['rows'], settings['columns']), dtype=np.uint16)
        img = get_frames(img_per_stack)
        img = [process_buffer(im) for im in img]
        dset[...] = img
        settings['Time'] = time.time()
        settings['Date'] = time.strftime("%x, %X")
        save_settings(dset, settings)
        dn_count += np.sum(img)
    return dn_count

def grab_GHV(fn, group_n, num_stacks, img_per_stack, gain_vals):
    dn_count = 0
    settings = {}
    f = h5py.File(fn, 'a')
    grp = f.create_group(group_n)
    for j in gain_vals:
        set_EMV(j)
        settings.update(get_settings())
        clear_ccd()
        grp_g = grp.create_group(group_n)
        for i in np.arange(num_stacks):
            dset = grp_g.create_dataset(str(i), (img_per_stack, settings['rows'], settings['columns']), dtype=np.uint16)
            img = get_frames(img_per_stack)
            img = [process_buffer(im) for im in img]
            dset[...] = img
            settings['Time'] = time.time()
            settings['Date'] = time.strftime("%x, %X")
            save_settings(dset, settings)
            dn_count += np.sum(img)
    return dn_count
        
    
def shutdown():
    ccd_off()
    close()
    

