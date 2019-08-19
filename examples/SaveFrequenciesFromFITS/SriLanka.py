# -*- coding: utf-8 -*-
"""
Created on Tue May 15 2015

@author: Christian Monstein
"""

import pyfits
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib import cm


files = 'ACCIMT-SRI_20150515_060000_59.fit.gz'

hdu = pyfits.open(files)
print hdu.info() # FIT-file structure

dB = hdu[0].data/255.0*2500.0/25.4 # conversion digits -> dB
mini_dB = np.min(dB) # find lowest value
rel_dB = dB-mini_dB # set background 0

freqs = hdu[1].data['Frequency'][0] # extract freqeuncy axis
time  = hdu[1].data['Time'][0] # extract time axis

extent = (time[0], time[-1], freqs[-1], freqs[0])

plt.imshow(rel_dB, aspect = 'auto', extent = extent, cmap=cm.jet) 
## cm.PRGn, cm.hot, cm.cool, cm.bone, cm.binary, cm.spectral, cm.jet
plt.xlabel('Time [s]')
plt.ylabel('Frequency [MHz]')
plt.title('FIT file Sri Lanka with frequecy table export')

cbar = plt.colorbar()
cbar.ax.set_ylabel('dB above background')

plt.show()

# Write frequencies to a local ASCII-file
c = np.array([freqs]).T
np.savetxt('frequencies.txt', c, fmt='%f')

# Write frequencies in reversed order  to a local ASCII-file
reversed_c = np.array([freqs]).T[::-1]
np.savetxt('frequencies_reversed.txt', reversed_c, fmt='%f')
