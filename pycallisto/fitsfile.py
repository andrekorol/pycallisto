# FitsFile: Classes and methods for reading data from FITS files
# Copyright (C) 2020 Andre Rossi Korol
#
# This file is part of PyCallisto.
# PyCallisto: Python tools for analyzing data from the e-Callisto International
# Network of Solar Radio Spectrometers
#
# PyCallisto is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyCallisto is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyCallisto. If not, see <https://www.gnu.org/licenses/>.


import fnmatch
import os
from pathlib import Path

import numpy as np
from astropy.io import fits

from pycallisto.fitserror import FitsFileError


class FitsFile(object):
    """Main entry point to the FITS file format."""

    def __init__(self, filename, filepath=""):
        self.filename = filename  # Name of the FITS file
        if filepath:
            self.filepath = Path(filepath)  # Path to the FITS file
        else:
            # Look for the file and set its path
            matches = []
            top_dir = os.getcwd()
            for root, _, files in os.walk(top_dir):
                for name in fnmatch.filter(files, self.filename):
                    matches.append(os.path.join(root, name))
            if not matches:
                error_message = f"{self.filename} was not found under the "
                error_message += f"current working directory ({top_dir})."
                raise FileNotFoundError(error_message)
            else:
                self.filepath = Path(matches[0])
        try:
            self.hdul = fits.open(self.filepath)  # List of HDUs
            # (Header Data Unit)
        except OSError:
            error_message = f"{self.filename} is not a valid FITS file "
            error_message += "(e.g., .fits, .fit, .fit.gz, .fts)"
            raise FitsFileError(error_message)


class ECallistoFitsFile(FitsFile):
    def __init__(self, filename, filepath=""):
        FitsFile.__init__(self, filename, filepath)

        # Extract the data from the FITS file Header Data Units
        hdul_dataset = {}
        hdul = self.hdul
        header = hdul[0].header  # Header of the primary HDU
        data = hdul[1].data  # Data of the first extension HDU
        # Data of the primary HDU
        hdul_dataset["data"] = hdul[0].data.astype(np.float32)
        hdul_dataset["v_min"] = -1  # -0.5, 100
        hdul_dataset["v_max"] = 8  # 4, 160
        hdul_dataset["dref"] = hdul_dataset["data"] - np.min(hdul_dataset["data"])
        # conversion digit->voltage->into db
        hdul_dataset["db"] = self.digit_to_voltage(hdul_dataset["dref"]) / 25.4
        hdul_dataset["db_median"] = np.median(hdul_dataset["db"], axis=1, keepdims=True)
        hdul_dataset["hh"] = float(header["TIME-OBS"].split(":")[0])
        hdul_dataset["mm"] = float(header["TIME-OBS"].split(":")[1])
        hdul_dataset["ss"] = float(header["TIME-OBS"].split(":")[2])
        hdul_dataset["time"] = data[0][0].astype(np.float32)
        hdul_dataset["f0"] = data[0][1].astype(np.float32)
        # cut lower 10 channels:
        hdul_dataset["frequency"] = hdul_dataset["f0"][:-10]
        hdul_dataset["start_time"] = (
            hdul_dataset["hh"] * 3600 + hdul_dataset["mm"] * 60 + hdul_dataset["ss"]
        )
        hdul_dataset["rows"] = hdul_dataset["data"].shape[0]
        hdul_dataset["columns"] = hdul_dataset["data"].shape[1]
        hdul_dataset["dt"] = hdul_dataset["time"][1] - hdul_dataset["time"][0]
        hdul_dataset["time_axis"] = (
            hdul_dataset["start_time"]
            + hdul_dataset["dt"] * np.arange(hdul_dataset["columns"])
        ) / 3600
        hdul_dataset["freq_axis"] = np.linspace(
            hdul_dataset["frequency"][0], hdul_dataset["frequency"][-1], 3600
        )

        # Update the instance's dataset
        self.hdul_dataset = hdul_dataset

        # Close the FITS file that was opened on the parent class
        hdul.close()

    @staticmethod
    def digit_to_voltage(digits: np.ndarray) -> np.ndarray:
        """Convert an HDU's image data from an array of digits, 
        to an array of decibels.

        :param digits: Array of digits obtained from a FITS file primary HDU data.
        :returns: Array of decibels.
        """
        return digits / 255.0 * 2500.0
