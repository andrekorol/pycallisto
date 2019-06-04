# Pycallisto: Python tools for analyzing data from the e-Callisto International
# Network of Solar Radio Spectrometers
# Copyright (C) 2019 Andre Rossi Korol
#
# This file is part of Pycallisto.
#
# Pycallisto is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pycallisto is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pycallisto. If not, see <https://www.gnu.org/licenses/>.


class FitsFileError(Exception):
    """Exception to be raised when astropy.io.fits.open is """
    def __init__(self, message):
        super().__init__(message)
