import sys
from PyQt4 import QtCore, QtGui
from ccam import Ui_MainWindow
import h5py
import pyqtgraph as pg
import numpy as np
import time
import xcam_helper as xc
timer = QtCore.QTimer()

class StartQT4(QtGui.QMainWindow):

    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        self.im = self.ui.graphicsView
        self.plt = self.ui.graphicsView_2
        timer.timeout.connect(self.updateImage)
        self.ui.ccdon.clicked.connect(self.setupCamera)
        self.ui.apply_settings.clicked.connect(self.getCameraSettings)
        self.ui.grab.clicked.connect(timer.start)
        self.ui.pause.clicked.connect(timer.stop)
        self.ui.captureprogress.setValue(0)
        self.timeseries = []
        self.userSettingsLoaded = False
        self.curImage = 0
        self.curImageSet = 0
        self.ui.readtime.setDigitCount(5)
        self.settings={}
        
    def setupCamera(self):
        print "dummy button!"
        
    def saveSettings(self):
        xc.save_settings(self.dset, self.settings)
        
        
    def updateImage(self):

            #Need to change the current HDF5 group
        #Get the image and save it to the hdf5 group

        t0 = time.time()
        self.settings['StartT'] = time.time()
        data = np.random.normal(100, 10, size=(500,500))
        #data = xc.get_frame()
        #self.settings['endT'] = time.time()
        self.ui.readtime.display(time.time() - t0)
        #data = xc.process_buffer(data)
        #self.dset[self.curImage,:,:] = data
        self.timeseries.append(np.sum(np.abs(data)))
        self.im.setImage(np.transpose(np.double(data)))

        self.plt.plot(self.timeseries)

        self.curImage += 1
        #self.saveSettings()
        time.sleep(.1)
        
    def testImage(self):
        #capture a test image and render it to the view
        self.testimage = 1

    def setupCamera(self):
        #load defaults to camera
        #render test image.
        self.testimage = 0

    def getCameraSettings(self):
        print "Entering getCameraSettings"
        self.ui.captureprogress.setValue(0)
        self.userSettingsLoaded = True
        self.settings['CDSgain'] = 10
        self.settings['CDSoffset'] = 40
        self.settings['integrationTime'] = int(self.ui.inttime_bx.text())
        self.settings['voltageFile'] = str(self.ui.vfile_bx.text())
        self.settings['parameterFile'] = str(self.ui.pfile_bx.text())
        self.settings['frameType'] = str(self.ui.framemode_bx.currentText())
        self.settings['timeUnits'] = str(self.ui.timeunits_bx.currentText())
        self.settings['rows'] = self.ui.rows_bx.value()
        self.settings['columns'] = self.ui.cols_bx.value()
        self.settings['outputfile'] = str(self.ui.outputfile_bx.text())
        self.settings['group'] = str(self.ui.groupname_bx.text())
        self.settings['numimages'] = self.ui.numimages_bx.value()
        self.settings['numimagesets'] = self.ui.numimagesets_bx.value()
        self.settings['beamEnergy'] = float(self.ui.beamenergy_bx.text())
        self.settings['normalisation'] = float(self.ui.normalisation_bx.text())
        self.settings['timeout'] = 30000
        self.curImage = 0
        self.curImageSet = 0

        self.f = h5py.File(self.settings['outputfile'], 'a')
        self.startImageSet = 0
        if self.ui.appendtogroup.isChecked() == True:
            grp = self.f[self.settings['group']]
            curmax = 0
            for dset in grp:

                if int(dset) > curmax:
                    curmax = int(dset)
            self.startImageSet = curmax + 1
            self.curImageSet = curmax + 1
            self.settings['numimagesets'] += curmax + 1
            self.grp = self.f[self.settings['group']]
            
        else:
            self.grp = self.f.create_group(self.settings['group'])

        print "Applying Settings"
        xc.apply_settings(self.settings)
        print "Settings Applied"
        xc.set_EMV(self.ui.hv_bx.value())
        xc.set_parallel_binning(1)
        xc.set_vss(int(self.ui.vss_bx.text()))
        xc.set_cds_gain(10)
        xc.set_cds_offset(40)
        
        #self.settings.update(xc.get_settings())
        # show current hdf5 structure
        self.ui.hdf5view.clear()
        for grp in self.f.values():
            self.ui.hdf5view.append(grp.name + ", ")

        self.dset = self.grp.create_dataset(str(self.curImageSet), (self.settings['numimages'], self.settings['rows'], self.settings['columns']))
        self.ui.captureprogress.setRange(0, self.settings['numimages']*self.settings['numimagesets'])
        print "done"

if __name__ == "__main__":
    # settings = {}
    # print "Settings up Camera"
    # settings['CDSgain'] = 10
    # settings['CDSoffset'] = 40
    # settings['sequencerFile'] = 'CCD97-14Bit.DEX'
    # settings['parameterFile'] = 'params.dat'
    # settings['voltageFile'] = 'voltages.dat'
    # settings['columns'] = 558
    # settings['rows'] = 2500
    # settings['frameType'] = 'FF'
    # settings['timeUnits'] = 'ms'
    # settings['timeout'] = 50000
    # settings['integrationTime'] = 1
    # xc.setup_camera(settings)

    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())