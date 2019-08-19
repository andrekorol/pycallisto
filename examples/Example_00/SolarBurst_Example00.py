# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 09:34:01 2014

@author: Christian Monstein
"""


import pyfits
import matplotlib.pyplot as plt 


files  = 'C:\Users\STEG\Desktop\MyPython\BLENSW_20140128_113000_59.fit.gz'

fds = pyfits.open(files)

data = fds[0].data

plt.imshow(data, aspect = 'auto')
plt.xlabel('Time [column number]')
plt.ylabel('Frequency [channel number]')
plt.title('Type II solar radio burst Bleien/Switzerland')

plt.show()