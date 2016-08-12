import numpy as np
import camera_settings
import h5py

#class to manager datasets etc.
class File:
    def __init__(self, fn):
        #initialise file
        self.filename = fn
        f = h5py.File(fn, 'a')
        f.close()
        self.curgroup = ''
        self.curdataset = 0
        
    def new_data(self, dat, settings):
        #find the current dataset index
        f = h5py.File(self.filename, 'a')
        if self.curgroup == '':
            return False
            
        grp = f[self.curgroup]
        print self.curdataset
        dset = grp.create_dataset(str(self.curdataset), data=dat)
        self.new_attributes(dset, settings)
        
        self.curdataset += 1
        f.close()
        return True

    def new_group(self, grp):
        f = h5py.File(self.filename, 'a')
        self.curgroup = grp
        
        if f.visit(lambda g: g == grp) == None:
            f.create_group(grp)
            f.close()
            return True
        else:
            cur = 0
            for dset in f[grp].keys():
                if (int(dset) >= cur):
                    cur = int(dset) + 1
            self.curdataset = cur
        f.close()
        return False
        
    def new_attributes(self, dset, settings):
        for key in settings:
            dset.attrs.create(key, settings[key])
        return

