import unittest
from pathlib import Path

from pycallisto import fitsplot

from .tools import get_test_file, sha3_512


class FitsPlotTestCase(unittest.TestCase):
    def setUp(self):
        self.original_file = Path("assets/test/BLEN7M_20110809_080004_25.fit.gz")
        self.original_image = "assets/test/BLEN7M_20110809_080004_25.png"
        self.test_file = get_test_file()
        self.test_image = Path("BLEN7M_20110809_080004_25.png")

        return super().setUp()

    def test_fits_plot(self):
        self.assertEqual(sha3_512(self.original_file), sha3_512(self.test_file))

        fitsplot.fits_plot(self.test_file, language="missing-language")
        self.assertEqual(sha3_512(self.original_image), sha3_512(self.test_image))

    def tearDown(self):
        self.test_file.unlink(missing_ok=True)
        self.test_image.unlink(missing_ok=True)

        return super().tearDown()
