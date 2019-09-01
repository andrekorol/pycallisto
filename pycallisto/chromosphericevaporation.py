# ChromosphericEvaporation: Class and methods for determining chromospheric
# evaporation front parameters
# Copyright (C) 2019 Andre Rossi Korol
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

import math

from pycallisto.fitsfile import ECallistoFitsFile


class ChromosphericEvaporationFitsFile(ECallistoFitsFile):
    def __init__(self, filename, filepath=""):
        ECallistoFitsFile.__init__(self, filename, filepath)
        self.front = {}

    def set_front_velocity(self, inf_front_time,
                           sup_front_time,
                           velocity=None):
        front = self.front
        if velocity is not None:
            front['velocity'] = velocity
        else:
            lin_reg_fn = self.get_fits_linear_regression_function()
            inf_front_freq = lin_reg_fn(inf_front_time)
            sup_front_freq = lin_reg_fn(sup_front_time)
            front['freq_diff'] = abs(sup_front_freq - inf_front_freq)

            inf_density = (inf_front_freq / 8.98e-03) ** 2
            sup_density = (sup_front_freq / 8.98e-03) ** 2
            front['density_diff'] = abs(sup_density - inf_density)

            Nq = 4.6e+8
            H = 7e+4
            inf_height = math.log(Nq / inf_density) * H
            sup_height = math.log(Nq / sup_density) * H

            front['time_diff'] = (sup_front_time - inf_front_time) * 3600
            front['height_diff'] = sup_height - inf_height
            front['df_over_dt'] = front['freq_diff'] / front['time_diff']

            self.front['velocity'] = round(front['height_diff'] /
                                           front['time_diff'], 1)

    def get_front_velocity(self):
        return self.front['velocity']

    def get_front(self):
        return self.front
