from sunpy.spectra.sources.callisto import CallistoSpectrogram
import matplotlib.pyplot as plt

files = 'C:\Users\STEG\Desktop\MyPython\BLENSW_20140128_113000_59.fit.gz'

image = CallistoSpectrogram.read(files)

image.plot()

plt.show()