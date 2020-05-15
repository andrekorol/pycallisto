from urldl import download

from pycallisto.fitsfile import ECallistoFitsFile

callisto_archives = "http://soleil80.cs.technik.fhnw.ch/" \
                    "solarradio/data/2002-20yy_Callisto/"
date_xpath = "2011/08/09/"
filename = "BLEN7M_20110809_083004_24.fit.gz"
download(callisto_archives + date_xpath + filename)

fits = ECallistoFitsFile(filename)
fits.plot_fits_linear_regression(True)
