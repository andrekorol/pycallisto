import os
import time
import unittest
from filecmp import cmp

import httpx
from matplotlib import pyplot as plt

from pycallisto import fitshelpers
from pycallisto.fitsfile import ECallistoFitsFile
from pycallisto.pycallistodata import LANGUAGES

from .tools import sha3_512


class FitsPlotTestCase(unittest.TestCase):
    def setUp(self):
        self.original_fitsfile = "assets/test/BLEN7M_20110809_080004_25.fit.gz"
        self.original_filename = "assets/test/BLEN7M_20110809_080004_25.png"

        # Download a FITS file from e-Callisto to use during the tests
        callisto_archives = (
            "http://soleil80.cs.technik.fhnw.ch/" "solarradio/data/2002-20yy_Callisto/"
        )
        date_xpath = "2011/08/09/"
        fitsfile = "BLEN7M_20110809_080004_25.fit.gz"
        fitsurl = callisto_archives + date_xpath + fitsfile

        self.test_fitsfile = "test_" + fitsfile

        with open(self.test_fitsfile, "wb") as fin:
            with httpx.stream("GET", fitsurl) as r:
                for chunk in r.iter_raw():
                    fin.write(chunk)

    def test_save_fits_figure(self):
        fitsfile = ECallistoFitsFile(self.test_fitsfile)
        plt.figure(1)

        plt.imshow(
            fitsfile.hdul_dataset["db"] - fitsfile.hdul_dataset["db_median"],
            cmap="magma",
            norm=plt.Normalize(
                fitsfile.hdul_dataset["v_min"], fitsfile.hdul_dataset["v_max"]
            ),
            aspect="auto",
            extent=[
                fitsfile.hdul_dataset["time_axis"][0],
                fitsfile.hdul_dataset["time_axis"][-1000],
                fitsfile.hdul_dataset["frequency"][-1],
                fitsfile.hdul_dataset["frequency"][0],
            ],
        )

        plt.gca().invert_yaxis()

        language = "en"

        try:
            labels = LANGUAGES[language.lower()]
        except KeyError:
            labels = LANGUAGES["en"]

        labels_fontsize = 15
        axis_params_labelsize = 14
        plt.xlabel(labels["xlabel"], fontsize=labels_fontsize)
        plt.ylabel(labels["ylabel"], fontsize=labels_fontsize)
        plt.tick_params(labelsize=axis_params_labelsize)

        fig = plt.gcf()

        self.test_filename = fitshelpers.save_fits_figure(fitsfile, fig, "png")

        self.assertEqual(sha3_512(self.original_fitsfile), sha3_512(self.test_fitsfile))
        self.assertEqual(sha3_512(self.original_filename), sha3_512(self.test_filename))

    def tearDown(self):
        os.remove(self.test_fitsfile)
        os.remove(self.test_filename)
