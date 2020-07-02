# FitsHelpers: Helper functions used throughout PyCallisto
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


from matplotlib.figure import Figure


def figure_config(**kwargs):
    """Get optional keyword arguments related to plt.figure."""
    return {
        "figsize": kwargs.pop("figsize", None),
        "dpi": kwargs.pop("dpi", None),
        "facecolor": kwargs.pop("facecolor", None),
        "edgecolor": kwargs.pop("edgecolor", None),
        "frameon": kwargs.pop("frameon", None),
        "FigureClass": kwargs.pop("FigureClass", Figure),
        "clear": kwargs.pop("clear", None),
    }


def imshow_config(**kwargs):
    """
    Get optional keyword arguments related to plt.imshow.
    The rest of the given keyword arguments are passed directly
    inside the fits_plot function call.
    """
    return {
        "cmap": kwargs.pop("cmap", "magma"),
        "aspect": kwargs.pop("aspect", "auto"),
    }
