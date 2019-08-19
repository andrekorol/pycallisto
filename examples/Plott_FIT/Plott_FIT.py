"""
# python script to plot and zoom/save FIT-files
# Created: Chr. Monstein 29.10.2017
# Updates: 
"""

from matplotlib import pyplot as plt
import numpy as np
from astropy.io import fits as pf
import os
from Tkinter import Tk
from tkFileDialog import askopenfilename

#-----------------------------------------------------------------------------

def Digit2Voltage(d):
    return d/255.0*2500.0
     
#-----------------------------------------------------------------------------
Tk().withdraw() # 
myfile = askopenfilename() # show an "Open" dialog box and return file
hdu = pf.open(myfile)
data = hdu[0].data.astype(np.float32)
date = hdu[0].header['DATE-OBS']
hh   = float(hdu[0].header['TIME-OBS'].split(":")[0]) 
mm   = float(hdu[0].header['TIME-OBS'].split(":")[1])
ss   = float(hdu[0].header['TIME-OBS'].split(":")[2]) 
time = hdu[1].data[0][0].astype(np.float32)
f0   = hdu[1].data[0][1].astype(np.float32)
rows = f0.shape[0]
frequency = f0[:-10] # cut lower 10 channels
hdu.close()

start_time = hh*60*60 + mm*60 + ss # all in seconds
ut = time + start_time

rows    = data.shape[0]
columns = data.shape[1]
print "Rows=",rows
print "Columns=",columns

dT = time[1]-time[0]
time_axis = (start_time + dT * np.arange(data.shape[1]))/3600

#-----------------------------------------------------------------------------
plt.figure(figsize=(11,6))
vmin = -1 # -0.5, 100
vmax = 8 # 4, 160
dref = data - np.min(data)
dB = Digit2Voltage(dref)/25.4 # conversion digit->voltage->into dB
dB_median = np.median(dB, axis=1,keepdims=True)

plt.imshow(dB-dB_median, 
           aspect="auto", 
           cmap="magma", # afmhot, CMRmap, gnuplot, rainbow, hot, hot_r, magma, inferno, plasma, jet, cubehelix
           extent=[time_axis[0], time_axis[-1000], frequency[-1], frequency[0]],
           norm=plt.Normalize(vmin, vmax)
          )
plt.colorbar(label="dB above background")
plt.xlabel("Time [UT]",fontsize=15)
plt.ylabel("Frequency",fontsize=15)
fnam = os.path.basename(myfile) # extract filename only
plt.title(fnam, fontsize=16)
plt.tick_params(labelsize=14)
plt.show()
plt.savefig(myfile + '.png',bbox_inches="tight")
    