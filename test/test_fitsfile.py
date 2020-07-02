import json
import os
import unittest
from pathlib import Path

from pycallisto import fitsfile
from pycallisto.fitserror import FitsFileError

from .tools import NumpyEncoder, get_test_file, sha3_512


class FitsFileTestCase(unittest.TestCase):
    def setUp(self):
        self.original_file = Path("assets/test/BLEN7M_20110809_080004_25.fit.gz")
        self.test_file = get_test_file()
        self.missing_file = "NOT_HERE_BLEN7M_20110809_080004_25.fit.gz"
        self.invalid_file = "assets/test/BLEN7M_20110809_080004_25.png"
        self.original_hdul_dataset = "assets/test/hdul_dataset.json"
        self.test_hdul_dataset = "hdul_dataset.json"

        return super().setUp()

    def test_fits_file(self):
        self.assertEqual(sha3_512(self.original_file), sha3_512(self.test_file))

        original_fits = fitsfile.FitsFile(self.test_file, self.original_file)
        self.assertEqual(self.original_file, original_fits.filepath)

        fits = fitsfile.FitsFile(self.test_file)
        self.assertEqual(self.test_file, fits.filename)

        with self.assertRaises(FileNotFoundError):
            fitsfile.FitsFile(self.missing_file)

        with self.assertRaises(FitsFileError):
            fitsfile.FitsFile(Path(self.invalid_file).name, self.invalid_file)

    def test_ecallisto_fits_file(self):
        ecallisto_fits = fitsfile.ECallistoFitsFile(self.test_file)
        with open(self.test_hdul_dataset, "w") as fin:
            json.dump(ecallisto_fits.hdul_dataset, fin, indent=2, cls=NumpyEncoder)

        self.assertEqual(
            sha3_512(self.original_hdul_dataset), sha3_512(self.test_hdul_dataset)
        )

    def tearDown(self):
        if os.path.isfile(self.test_file):
            os.remove(self.test_file)

        if os.path.isfile(self.test_hdul_dataset):
            os.remove(self.test_hdul_dataset)

        return super().tearDown()
