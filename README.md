# xcamCaVA
Software for operating the xcam CaVa camera system.
## Usage
The module currently contains 3 classes. CameraSettings provides some helper functions and stores the operating voltages and various parameters of the camera system. Modifications to the camera parameters should be applied to this class and then fed into the CameraInterface() class via the apply_settings() method, which takes an instance of the CameraSettings class.

The Camera class provides access to the xcam dll, and can be used without the other helper classes for more direct control.

## Installation
Download the package. Navigate to the top level directory containing setup.py. 
Execute: python setup.py install
Note: the xcam dll and a camera system + ccd are required to use this module.
## Example Program
The following program initialises the camera system, grabs a single image and display it, before shutting down the CCD and exiting.
```python
import camera_interface as cmi
import camera_settings as cset
import numpy as np
import matplotlib.pyplot as plt
import time

#applying camera settings
settings = cset.CameraSettings()
settings.rows = 1056
settings.sequencerfile = 'CCD97-14Bit.DEX'
settings.columns = 552
settings.timeout = 30000
settings.frametype = 'FF'
settings.timeunits = 'ms'
settings.integrationtime = 1000
settings.cdsgain = 40
settings.cdsoffset = 10
settings.read_parameter_file("params.dat") #text file of parameter values
settings.read_voltage_file("voltages.dat") #text file of voltage values
settings.set_voltage('vss', 96)
settings.set_voltage('emv', 0)
settings.set_param('parallelbinning', 1)

inter = cmi.CameraInterface() #initialise the camera system
inter.update_settings(settings) #apply the user settings
err, img = inter.get_image() # grab and image from the ccd
img = inter.process_buffer(img) #process the raw image data

#Display
plt.imshow(img, interpolation='None') 
plt.show()

#
inter.shutdown()
```
