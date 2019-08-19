# Using SunPy to plot FIT-files including x-axis (time)
# Christian Monstein, 15.05.2015
# C:\Users\STEG\Desktop\MyPython\SolarBurst_Example03.py

from sunpy.spectra.sources.callisto import CallistoSpectrogram

file = 'C:\Users\STEG\Desktop\MyPython\BLENSW_20140128_113000_59.fit.gz'

from matplotlib import pyplot as plt
from matplotlib import cm

image = CallistoSpectrogram.read(file)
image.plot()
plt.show()

nobg = image.subtract_bg()
nobg.plot(cmap=cm.jet,vmin=-17) 
# binary / .hot / .PRGn / jet / gray /gist_yarg / spectral; +/-25 digit

plt.ylabel("Frequency [MHz]")
plt.xlabel("Time [UT]")
#plt.title("Bleien low frequncy antenna")
plt.show()


spectrum = image[ 77 , :] # Single Lightcurve at channel 77
plt.plot(spectrum,linewidth=2.0)
plt.ylabel('Intensity')
plt.xlabel('Time [sample]')
plt.title('Lightcurve')
plt.axis([0, 3600, 120, 200])
plt.grid(True)
plt.plot()
plt.show()

spectrum = image[ : , 77] # Single spectrum at sample 77
plt.plot(spectrum, linewidth=2.0)
plt.ylabel('Intensity')
plt.xlabel('Channel number')
plt.title('Spectrum')
plt.plot()
plt.show()

bg = image.auto_const_bg() ## background
bg = image[:,55] # specific channel
print image.freq_axis
plt.plot(image.freq_axis, bg, linewidth=3.0)
plt.xlabel("Frequency [MHz]")
plt.ylabel("Intensity")
plt.show() 