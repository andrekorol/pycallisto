# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 09:34:01 2014

@author: Christian Monstein
"""


import pyfits
import matplotlib.pyplot as plt 


files = 'C:\Users\STEG\Desktop\MyPython\BLENSW_20140128_113000_59.fit.gz'


fds = pyfits.open(files)

data = fds[0].data

freqs = fds[1].data['frequency'][0]
time = fds[1].data['time'][0]

extent = (time[0], time[-1], freqs[-1], freqs[0])


plt.imshow(data, aspect = 'auto', extent = extent)
plt.xlabel('Time [s]')
plt.ylabel('Frequency [MHz]')
plt.title('Type III burst with physical axis label')

plt.show()