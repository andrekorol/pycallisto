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


import collections.abc
import itertools
from datetime import timedelta
from pathlib import Path, PurePath
from typing import Sequence, Union

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from .fitsfile import ECallistoFitsFile
from .fitshelpers import figure_config, imshow_config
from .pycallistodata import LANGUAGES


def fitsplot(
    fits: Union[str, Sequence[str]],
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

    if isinstance(fits, collections.abc.Sequence):
        filenames = sorted(fits)
    else:
        filenames = [fits]

    for fname in filenames:
        fitsfile = ECallistoFitsFile(fname)

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

    hours_xticks = []
    locs, _ = plt.xticks()
    for loc in locs:
        hour = str(int(loc)) + ":" + str(int((loc - int(loc)) * 60))
        if hour.split(":")[-1] == "0":
            hour += "0"
        if len(hour.split(":")[-1]) == 1:
            hour = hour.split(":")[0] + ":0" + hour.split(":")[-1]
        hours_xticks.append(hour)

    initial_hour = timedelta(hours=round(ext_time_axis[0], 2))

    initial_seconds = initial_hour.seconds
    initial_xticks_seconds = int(hours_xticks[0].split(":")[0]) * 3600
    initial_xticks_seconds += int(hours_xticks[0].split(":")[-1]) * 60

    if initial_seconds != initial_xticks_seconds:
        hours_xticks.pop(0)
        locs = locs[1:]

    for index, item in enumerate(hours_xticks):
        if len(item.split(":")[0]) == 1:
            hours_xticks[index] = "0" + item

    final_hour = timedelta(hours=round(ext_time_axis[-1], 2))
    final_seconds = final_hour.seconds
    final_xticks_seconds = int(hours_xticks[-1].split(":")[0]) * 3600
    final_xticks_seconds += int(hours_xticks[-1].split(":")[-1]) * 60

    if final_seconds != final_xticks_seconds:
        hours_xticks.pop()
        locs = locs[:-1]

    if initial_xticks_seconds != initial_seconds:
        last_minutes = int(hours_xticks[-1].split(":")[0]) * 60
        last_minutes += int(hours_xticks[-1].split(":")[-1])
        first_minutes = int(hours_xticks[0].split(":")[0]) * 60
        first_minutes += int(hours_xticks[0].split(":")[-1])
        minutes_delta = last_minutes - first_minutes
        ticks_interval = int(round(minutes_delta / (len(locs) - 1), 0))
        final_xticks = []
        hour = timedelta(minutes=first_minutes)
        final_xticks.append(":".join(hour.__str__().split(":")[:-1]))

        for _ in itertools.repeat(None, len(locs) - 1):
            hour = hour + timedelta(minutes=ticks_interval)
            final_xticks.append(":".join(hour.__str__().split(":")[:-1]))

        plt.xticks(locs, final_xticks)

    else:
        hours_delta = round(ext_time_axis[-1], 2)
        hours_delta -= round(ext_time_axis[0], 2)
        minutes_delta = hours_delta * 60
        ticks_interval = int(round(minutes_delta / (len(locs) - 1), 0))
        final_xticks = []
        hour = initial_hour
        final_xticks.append(":".join(hour.__str__().split(":")[:-1]))

        for _ in itertools.repeat(None, len(locs) - 1):
            hour = hour + timedelta(minutes=ticks_interval)
            final_xticks.append(":".join(hour.__str__().split(":")[:-1]))

        plt.xticks(locs, final_xticks)

    final_hour_str = final_hour.__str__()
    if len(final_hour_str.split(":")[0]) == 1:
        final_hour_str = "0" + final_hour_str

    # Define plot's title
    first_fname = str(filenames[0])
    last_fname = str(filenames[-1])
    title_start = "_".join(first_fname.split("_")[:-1])
    freq_band = last_fname.split("_")[-1].split(".")[0]
    title_end = "".join(final_hour_str.split(":"))
    title_end = "_".join([title_end, freq_band])
    title = "_".join([title_start, title_end])
    plt.title(title, fontsize=16)

    # Get the current figure to save it after showing it
    fig = plt.gcf()

    if show:
        plt.show()

    if save:
        fitspath = fitsfile.filepath
        img_filepath = str(fitspath).replace(fitspath.name, title + ext)
        fig.savefig(img_filepath)

    plt.clf()
    plt.cla()
    plt.close("all")
