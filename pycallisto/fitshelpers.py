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


import asyncio
import pathlib
from concurrent.futures import ThreadPoolExecutor
from typing import List

from matplotlib import figure
from matplotlib import pyplot as plt

from pycallisto.fitsfile import ECallistoFitsFile


def savefigure(fitsfile: ECallistoFitsFile, fig: figure.Figure, ext: str) -> str:
    """Get the filename of a given FITS file and then use it to save
    the figure with a given extension.

    :param fitsfile: Instance of a FITS file to get the filename from.
    :param fig: Figure to be saved.
    :param ext: Extension used when saving the figure to a file.
    :returns: Name of the saved file.
    """

    # Remove possible leading period from the extension since it will
    # added when forming the filename
    if ext[0] == ".":
        ext = ext[1:]

    # Remove ".fit.gz" from FITS files that came from e-Callisto
    # and add the new file extension
    filename = ".".join([pathlib.PurePath(fitsfile.filepath).stem.split(".")[0], ext])

    fig.savefig(filename, bbox_inches="tight")  # TODO Check meaning of bbox_inches

    return filename


async def savefits(
    fitsfile: ECallistoFitsFile, fig: figure.Figure, ext: str
) -> List[str]:
    """Wrap the savefigure function in a Future and schedule it to
    execute asynchronously on a pool of threads.

    :param fitsfile: Instance of a FITS file to get the filename from.
    :param fig: Figure to be saved.
    :param ext: Extension used when saving the figure to a file.
    :returns: List with string containing the result of awaiting the
    Future.
    """
    with ThreadPoolExecutor(1) as executor:
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(executor, savefigure, fitsfile, fig, ext)
        return await asyncio.gather(future)


def save_fits_figure(fitsfile: ECallistoFitsFile, fig: figure.Figure, ext: str) -> str:
    """Create an event loop to run the savefits Future on its
    ThreadPoolExecutor and get the name of the saved file.

    :param fitsfile: Instance of a FITS file to get the filename from.
    :param fig: Figure to be saved.
    :param ext: Extension used when saving the figure to a file.
    :returns: Name of the saved file.
    """
    loop = asyncio.get_event_loop()
    filename = loop.run_until_complete(savefits(fitsfile, fig, ext))[0]
    # loop.close()

    return filename
