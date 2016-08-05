import h5py
import numpy as np
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
import matplotlib.pyplot as plt

#find xrays
def find_xr(img):
    img = np.double(img)
    mn = np.mean(img)
    std = np.std(img)
    thresh = mn + 3*std
    x, y = [], []
    for i in range(len(img[:,0]) - 1):
        for j in range(len(img[0,:]) - 1):
            if(img[i,j] > thresh):
                x.append(i)
                y.append(j)
    vals = []
    for xi,yi in zip(x,y):
        tot = 0
        ind = np.arange(-1, 2, 1)
        for v in ind:
            for z in ind:
                tot += img[xi + v, yi + z]
        vals.append(tot - 9*mn)
    return np.asarray(zip(x,y,vals))


img = np.random.normal(100, 10, size=(500, 500))
rcoord = np.random.randint(0,500,size=(100, 2))
for i in rcoord:
    img[i[0], i[1]] += 690

coords = find_xr(img)

print len(coords)
for i,j,val in coords:
    print val
    
