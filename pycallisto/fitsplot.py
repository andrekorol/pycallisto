# FitsPlot: Functions for plotting data from FITS files
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


from pathlib import PurePath
from typing import Sequence

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from .fitsfile import ECallistoFitsFile
from .fitshelpers import figure_config, imshow_config
from .pycallistodata import LANGUAGES


def fits_plot(
    filename: str,
    ext: str = ".png",
    show_colorbar: bool = False,
    show: bool = True,
    save: bool = True,
    language: str = "en",
    labels_fontsize: int = 15,
    axis_params_labelsize: int = 14,
    **kwargs
):
    fitsfile = ECallistoFitsFile(filename)

    plt.figure(1, **figure_config(**kwargs))

    plt.imshow(
        fitsfile.hdul_dataset["db"] - fitsfile.hdul_dataset["db_median"],
        **imshow_config(**kwargs),
        norm=plt.Normalize(
            fitsfile.hdul_dataset["v_min"], fitsfile.hdul_dataset["v_max"]
        ),
        extent=[
            fitsfile.hdul_dataset["time_axis"][0],
            fitsfile.hdul_dataset["time_axis"][-1000],
            fitsfile.hdul_dataset["frequency"][-1],
            fitsfile.hdul_dataset["frequency"][0],
        ],
        **kwargs
    )

    # Follow the convention of inverting the Frequency axis
    plt.gca().invert_yaxis()

    # Get the labels to use when plotting
    try:
        labels = LANGUAGES[language.lower()]
    except KeyError:
        # Defaults to English if an invalid or missing language is given.
        # Check languages.json for the currently supported languages.
        # Feel free to add a new language by adding it to languages.json
        # and then sending a Pull Request.
        labels = LANGUAGES["en"]

    if show_colorbar:
        cb = plt.colorbar()
        cb.set_label(label=labels["colorbar"], fontsize=labels_fontsize)

    plt.xlabel(labels["xlabel"], fontsize=labels_fontsize)
    plt.ylabel(labels["ylabel"], fontsize=labels_fontsize)
    plt.tick_params(labelsize=axis_params_labelsize)

    # Get the current figure to save it after showing it
    fig = plt.gcf()

    if show:
        plt.show()

    if save:
        fitspath = fitsfile.filepath
        img_filepath = str(fitspath).replace("".join(fitspath.suffixes), ext)
        fig.savefig(img_filepath)


def fits_plot_list(
    filenames: list,
    ext: str = ".png",
    show_colorbar: bool = False,
    show: bool = True,
    save: bool = True,
    language: str = "en",
    labels_fontsize: int = 15,
    axis_params_labelsize: int = 14,
    **kwargs
):
    extended_db = None
    ext_time_axis = None
    plt.figure(1, **figure_config(**kwargs))

    for fits in filenames:
        fitsfile = ECallistoFitsFile(fits)

        if extended_db is None and ext_time_axis is None:
            extended_db = fitsfile.hdul_dataset["db"]
            ext_time_axis = fitsfile.hdul_dataset["time_axis"]
        else:
            extended_db = np.hstack((extended_db, fitsfile.hdul_dataset["db"]))
            ext_time_axis = np.hstack(
                (ext_time_axis, fitsfile.hdul_dataset["time_axis"])
            )

    extended_db_median = np.median(extended_db, axis=1, keepdims=True)
    plt.imshow(
        extended_db - extended_db_median,
        **imshow_config(**kwargs),
        norm=plt.Normalize(
            fitsfile.hdul_dataset["v_min"], fitsfile.hdul_dataset["v_max"]
        ),
        extent=[
            ext_time_axis[0],
            ext_time_axis[-1],
            fitsfile.hdul_dataset["frequency"][-1],
            fitsfile.hdul_dataset["frequency"][0],
        ],
        **kwargs
    )

    # Follow the convention of inverting the Frequency axis
    plt.gca().invert_yaxis()

    # Get the labels to use when plotting
    try:
        labels = LANGUAGES[language.lower()]
    except KeyError:
        # Defaults to English if an invalid or missing language is given.
        # Check languages.json for the currently supported languages.
        # Feel free to add a new language by adding it to languages.json
        # and then sending a Pull Request.
        labels = LANGUAGES["en"]

    if show_colorbar:
        cb = plt.colorbar()
        cb.set_label(label=labels["colorbar"], fontsize=labels_fontsize)

    plt.xlabel(labels["xlabel"], fontsize=labels_fontsize)
    plt.ylabel(labels["ylabel"], fontsize=labels_fontsize)
    plt.tick_params(labelsize=axis_params_labelsize)

    # Get the current figure to save it after showing it
    fig = plt.gcf()

    if show:
        plt.show()

    if save:
        fitspath = fitsfile.filepath
        img_filepath = str(fitspath).replace("".join(fitspath.suffixes), ext)
        fig.savefig(img_filepath)
