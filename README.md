<p align="center"><img src="assets/img/pycallisto_logo_200px.png" alt="PyCallisto Logo" style="width: 50%; height: 50%;" /></p>

<h2 align="center">Python library for analyzing data from the e-Callisto International Network of Solar Radio Spectrometers</h1>

<p align="center">
<a href="https://github.com/andrekorol/pycallisto/blob/master/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" /></a>
</p>

## Installation and usage

### Installation

<span style="font-weight: bold;">⚠️WARNING⚠️ PyCallisto is still under development, and breaking changes should be expected.</span>

PyCallisto is not available on [PyPi](https://pypi.org/) yet but, if you have Git installed, you can get it with:

`git clone https://github.com/andrekorol/pycallisto.git`

Otherwise, download it from https://github.com/andrekorol/pycallisto/archive/master.zip and unzip the master branch.

Once inside the package top directory, run the `python setup.py install` as usual.

### Usage

To test the library and its simplicity with some sample data, download these two FITS files from e-Callisto ([BLEN7M_20110809_080004_25.fit.gz](http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/2011/08/09/BLEN7M_20110809_080004_25.fit.gz) and [BLEN7M_20110809_081504_25.fit.gz](http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/2011/08/09/BLEN7M_20110809_081504_25.fit.gz)) and then run the following code from a Python interpreter:

```Python
from pycallisto import fitsfile

fits_file_list = [
    "BLEN7M_20110809_080004_25.fit.gz",
    "BLEN7M_20110809_081504_25.fit.gz",
]

fitsfile.ECallistoFitsFile.plot_fits_files_list(fits_file_list)
```

The resulting plot is:

<p align="center"><img src="assets/img/BLEN7M_20110809_080004_083000_25.png" alt="BLEN7M_20110809_080004_083000_25.png" /></p>
