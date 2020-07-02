import unittest
from pathlib import Path

from pycallisto import fitsplot

from .tools import get_test_file, get_test_file_list, sha3_512


class FitsPlotTestCase(unittest.TestCase):
    def setUp(self):
        self.original_file = Path("assets/test/BLEN7M_20110809_080004_25.fit.gz")
        self.original_image = "assets/test/BLEN7M_20110809_080004_25.png"
        self.test_file = get_test_file()
        self.test_image = Path("BLEN7M_20110809_080004_25.png")

        list_dir = Path("assets/test/list")
        self.original_file_list = sorted([fits for fits in list_dir.iterdir()])
        self.original_list_image = "assets/test/BLEN7M_20110216_153019_24.png"
        self.test_file_list = get_test_file_list()
        self.test_list_image = Path("BLEN7M_20110216_153019_24.png")

        return super().setUp()

    def test_fits_plot(self):
        self.assertEqual(sha3_512(self.original_file), sha3_512(self.test_file))

        fitsplot.fits_plot(
            self.test_file, show_colorbar=True, language="missing-language"
        )
        self.assertEqual(sha3_512(self.original_image), sha3_512(self.test_image))

    def test_fits_plot_list(self):
        for i in range(len(self.original_file_list)):
            self.assertEqual(
                sha3_512(self.original_file_list[i]), sha3_512(self.test_file_list[i])
            )

        fitsplot.fits_plot_list(
            self.test_file_list, show_colorbar=True, language="missing-language"
        )
        self.assertEqual(
            sha3_512(self.original_list_image), sha3_512(self.test_list_image)
        )

    def tearDown(self):
        self.test_file.unlink(missing_ok=True)
        self.test_image.unlink(missing_ok=True)

        for test_file in self.test_file_list:
            test_file.unlink(missing_ok=True)

        self.test_list_image.unlink(missing_ok=True)

        return super().tearDown()
