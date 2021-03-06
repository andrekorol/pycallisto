<p align="center"><img src="assets/img/pycallisto_logo_200px.png" alt="PyCallisto Logo" style="width: 50%; height: 50%;" /></p>

<h2 align="center">Python library for analyzing data from the e-Callisto International Network of Solar Radio Spectrometers</h1>

<p align="center">
<a href="https://travis-ci.com/github/andrekorol/pycallisto"><img alt="[Build Status" src="https://travis-ci.com/andrekorol/pycallisto.svg?branch=dev" /></a>
<a href="https://codecov.io/gh/andrekorol/pycallisto"><img alt="codecov" src="https://codecov.io/gh/andrekorol/pycallisto/branch/dev/graph/badge.svg" /></a>
<a href="https://github.com/andrekorol/pycallisto/blob/master/LICENSE"><img alt="License: GPL v3" src="https://img.shields.io/badge/License-GPLv3-blue.svg" /></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fandrekorol%2Fpycallisto?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fandrekorol%2Fpycallisto.svg?type=shield"/></a>
</p>

## Installation and usage

### Installation

**_⚠️WARNING⚠️ PyCallisto is still under development! Improvements and breaking changes should be expected in upcoming releases!_**

PyCallisto is not available on [PyPi](https://pypi.org/) yet but, you can download a development release at https://github.com/andrekorol/pycallisto/releases.

Otherwise, if you have Git installed and want to test the current unreleased version of PyCallisto, you can get the master branch with:

`git clone https://github.com/andrekorol/pycallisto.git`

Once inside the package top directory, run `python setup.py install` **OR** `pip install .`.

### Usage

To test the library and its simplicity with some sample data, download these two FITS files from e-Callisto ([BLEN7M_20110809_080004_25.fit.gz](http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/2011/08/09/BLEN7M_20110809_080004_25.fit.gz) and [BLEN7M_20110809_081504_25.fit.gz](http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/2011/08/09/BLEN7M_20110809_081504_25.fit.gz)) and then run the following code from a Python interpreter:

```Python
from pycallisto import fitsplot

fits_file_list = [
    "BLEN7M_20110809_080004_25.fit.gz",
    "BLEN7M_20110809_081504_25.fit.gz",
]

fitsplot(fits_file_list, show_colorbar=True)
```

The resulting plot is:

<p align="center"><img src="examples/BLEN7M_20110809_080004_083000_25.png" alt="BLEN7M_20110809_080004_083000_25.png" /></p>

## [License](https://github.com/andrekorol/pycallisto/blob/master/LICENSE)

PyCallisto is [free software](https://www.gnu.org/philosophy/free-sw.en.html): you can redistribute it and/or modify
it under the terms of the [GNU General Public License](<https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)>) as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fandrekorol%2Fpycallisto.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fandrekorol%2Fpycallisto?ref=badge_large)
