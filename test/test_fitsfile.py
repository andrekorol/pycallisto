import os
import unittest

import httpx

from pycallisto import fitsfile

from .tools import sha3_512


class FitsFileTestCase(unittest.TestCase):
    def setUp(self):
        self.original_file = "assets/test/BLEN7M_20110809_080004_25.fit.gz"
        self.test_file = "BLEN7M_20110809_080004_25.fit.gz"

        # Download a FITS file from e-Callisto to use during the tests
        callisto_archives = (
            "http://soleil80.cs.technik.fhnw.ch/" "solarradio/data/2002-20yy_Callisto/"
        )

        date_xpath = "2011/08/09/"
        fitsfile = "BLEN7M_20110809_080004_25.fit.gz"
        fitsurl = callisto_archives + date_xpath + fitsfile

        with open(self.test_file, "wb") as fin:
            with httpx.stream("GET", fitsurl) as r:
                for chunk in r.iter_raw():
                    fin.write(chunk)

        return super().setUp()

    def test_fits_file(self):
        self.assertEqual(sha3_512(self.original_file), sha3_512(self.test_file))

        fits = fitsfile.FitsFile(self.test_file)

        self.assertEqual(self.test_file, fits.filename)

    def tearDown(self):
        if os.path.isfile(self.test_file):
            os.remove(self.test_file)

        return super().tearDown()
