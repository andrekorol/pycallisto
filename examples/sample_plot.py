from pycallisto import fitsfile


fits_file_list = ["BLEN7M_20110809_080004_25.fit.gz", 
                  "BLEN7M_20110809_081504_25.fit.gz"]

fitsfile.ECallistoFitsFile.plot_fits_files_list(fits_file_list)