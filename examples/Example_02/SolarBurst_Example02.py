# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 09:34:01 2014

@author: Christian Monstein
"""

import pyfits
import matplotlib.pyplot as plt 
from matplotlib import cm

files = 'C:\Users\STEG\Desktop\MyPython\BLENSW_20140128_113000_59.fit.gz'

fds = pyfits.open(files)

data = fds[0].data
#data = data - data[7,:]# subtrahiere Spalte 7
data = data - data.mean(axis=1, keepdims=True) + 4 # subtract mean and add offset (1...50)
data = data.clip(-5,120) # limit peak values
data = data * 2500.0/255.0/25.4 # digit->dB

freqs = fds[1].data['frequency'][0]
time = fds[1].data['time'][0]

extent = (time[0], time[-1], freqs[-1], freqs[0])

plt.imshow(data, aspect = 'auto', extent = extent,cmap=cm.hot) ## cm.PRGn, cm.hot, cm.cool, cm.bone, cm.binary
plt.xlabel('Time [s]')
plt.ylabel('Frequency [MHz]')
plt.title('Type III burst with background subtracted')

cbar = plt.colorbar()
cbar.ax.set_ylabel('dB above background')

plt.show()