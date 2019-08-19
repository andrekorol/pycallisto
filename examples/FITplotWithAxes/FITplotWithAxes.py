# -*- coding: utf-8 -*-
"""
Created on Tue JUL 19 2016
Updated on Thu OCT 19 2017

@author: Christian Monstein
"""

import pyfits
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib import cm
import scipy as sp
from scipy import ndimage
import pylab as mplot
import sys

#------------------------------------------------------------------------------
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
#------------------------------------------------------------------------------
files = 'BIR_20150311_161500_02.fit.gz' # local data file
fmin = 100.0 # minimum frequency in MHz
fmax = 190.0 # maximum frequency in MHz
tmin = '16:20:00' # enter start-time here as hh:mm:ss
tmax = '16:30:00' # enter stop-time here as hh:mm:ss
#------------------------------------------------------------------------------

hdu = pyfits.open(files)
print hdu.info() # FIT-file structure

dB = hdu[0].data.astype(np.float32)/255.0*2500.0/25.4 # conversion digits -> dB
mini_dB = np.min(dB) # find lowest value
rel_dB = dB - mini_dB # set background 0

freqs = hdu[1].data['Frequency'][0] # extract frequency axis
time  = hdu[1].data['Time'][0] # extract time axis
hdu.close()

extent = (time[0], time[-1], freqs[-1], freqs[0])

rel_dB = rel_dB - rel_dB.mean(axis=1, keepdims=True)  # subtract average 
rel_dB = rel_dB.clip(-2,12) # limit peak values +/-
#------------------------------------------------------------------------------
plt.figure(figsize=(15,8))
plt.imshow(rel_dB, aspect = 'auto', extent = extent, cmap=cm.hot) 
## cm.PRGn, cm.hot, cm.cool, cm.bone, cm.binary, cm.spectral, cm.jet
plt.tick_params(labelsize=14)
plt.xlabel('Time [s]',fontsize=15)
plt.ylabel('Frequency [MHz]',fontsize=15)
plt.title('FIT file presentation as raw data, full size',fontsize=15)

cbar = plt.colorbar()
cbar.ax.set_ylabel('dB above background',fontsize=15)
plt.savefig('2D_raw.png')

#------------------------------------------------------------------------------

plt.figure(figsize=(15,8))
sigma = [0,1] # number of pixels for smoothing in y- and x-direction
blur = sp.ndimage.filters.gaussian_filter(rel_dB, sigma, mode='constant')
vmin = -2 # minimum color table in dB (-4.... 0)
vmax = 15 # maximum color table in dB (10....20)
plt.imshow(blur, aspect = 'auto', extent = extent, cmap=cm.hot_r,
           norm=plt.Normalize(vmin, vmax)) # defines image contrast
## cm.PRGn, cm.hot, cm.cool, cm.bone, cm.binary, cm.spectral, cm.jet

plt.xlim((400,900)) # x-axis limits in seconds
plt.ylim((fmin,fmax)) # y-axis limits in MHz
plt.tick_params(labelsize=14)
plt.xlabel('Time [s]',fontsize=15)
plt.ylabel('Frequency [MHz]',fontsize=15)
plt.title('FIT file presentation as Gaussian smoothed data, zoomed',fontsize=15)

cbar = plt.colorbar()
cbar.ax.set_ylabel('dB above background',fontsize=15)
plt.savefig('2D_smooth.png')
#------------------------------------------------------------------------------
# Here begins the complicated part with x-axis in hh:mm:ss
hh = float(pyfits.open(files)[0].header['TIME-OBS'].split(":")[0])
mm = float(pyfits.open(files)[0].header['TIME-OBS'].split(":")[1])
ss = float(pyfits.open(files)[0].header['TIME-OBS'].split(":")[2])
start_time = hh*3600 + mm*60 + ss
ut = time + start_time

k = 0 # index to search for frequencies in list
for f in freqs:
    if (f > fmin):
        klow = k
    if (f > fmax):
        khigh = k
    k = k + 1

dt = pyfits.open(files)[0].header['CDELT1'] # read time resolution from FIT-file
print dt
secmin = (float(int(tmin[0:2])*3600 + int(tmin[3:5])*60 + int(tmin[6:8])) - ut[0])
secmax = (float(int(tmax[0:2])*3600 + int(tmax[3:5])*60 + int(tmax[6:8])) - ut[0])
offset = 1.0 # correction for finite error in timing [sec]
xmin = (secmin+offset)/dt
xmax = (secmax+offset)/dt

mplot.figure(figsize=(15,10))
ax = mplot.subplot(111)
mplot.axis([xmin,xmax, klow, khigh]) # pixel values of the image
number_of_labels = 6
mplot.xticks(np.arange(xmin, xmax+1, (xmax-xmin)/number_of_labels))

vmin = 0 # minimum color table in dB (-4.... 0)
vmax = 12 # maximum color table in dB (10....20)
mplot.imshow(blur,aspect = 'auto',cmap=cm.inferno,norm=plt.Normalize(vmin, vmax)) 
# cmap=cm.gnuplot, gnuplot2, CMRmap, plasma, inferno, magma
cb1 = mplot.colorbar(orientation='vertical', shrink=0.99)
cb1.set_label('dB above background',fontsize=15)
cb1.ax.tick_params(labelsize=15) 

a = ax.get_xticks().tolist()
b = ax.get_yticks().tolist()
ahms=[]
for j in range(len(a)-1):
    sec = float(ut[int(a[j])])
    hh  = int(sec)/60/60
    mm  = int(sec - hh*60*60)/60
    ss  = int(sec - hh*60*60 - mm*60)
    ahms.append( '{:02d}:{:02d}:{:02d}'.format(hh,mm,ss))

for j in range(len(b)-1):
    ff = float(freqs[int(b[j])])
    b[j]=str(ff)[:5]

ax.set_xticklabels(ahms, fontsize=15)
ax.set_yticklabels(b, fontsize=15)

mplot.ylabel('Plasma frequency [MHz]', fontsize=18)
mplot.xlabel('Time [UT]', fontsize=18)

mplot.title(files, fontsize=20)
mplot.savefig('2D_smooth_with_axes.png',bbox_inches='tight')
#sys.exit()
#------------------------------------------------------------------------------
