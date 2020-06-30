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


import plotly.express as px
import plotly.tools as tls
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from .fitsfile import ECallistoFitsFile
from .pycallistodata import LANGUAGES


def fits_plot(
    filename: str,
    ext: str = "png",
    show_colorbar: bool = False,
    show: bool = True,
    save: bool = True,
    language: str = "en",
    labels_fontsize: int = 15,
    axis_params_labelsize: int = 14,
    **kwargs
):
    fitsfile = ECallistoFitsFile(filename)

    # Get optional keyword arguments related to plt.figure
    figsize = kwargs.pop("figsize", None)
    dpi = kwargs.pop("dpi", None)
    facecolor = kwargs.pop("facecolor", None)
    edgecolor = kwargs.pop("edgecolor", None)
    frameon = kwargs.pop("frameon", None)
    FigureClass = kwargs.pop("FigureClass", Figure)
    clear = kwargs.pop("clear", None)

    fig = px.imshow(fitsfile.hdul_dataset["db"] - fitsfile.hdul_dataset["db_median"])
    print(fig)
    fig.show()
    return

    plt.figure(
        1,
        figsize=figsize,
        dpi=dpi,
        facecolor=facecolor,
        edgecolor=edgecolor,
        frameon=frameon,
        FigureClass=FigureClass,
        clear=clear,
    )

    # Get optional keyword arguments related to plt.imshow
    # The rest of the given keyword arguments are passed directly
    # inside the function call
    cmap = kwargs.pop("cmap", "magma")
    aspect = kwargs.pop("aspect", "auto")

    # plt.imshow(
    #     fitsfile.hdul_dataset["db"] - fitsfile.hdul_dataset["db_median"],
    #     cmap=cmap,
    #     norm=plt.Normalize(
    #         fitsfile.hdul_dataset["v_min"], fitsfile.hdul_dataset["v_max"]
    #     ),
    #     aspect=aspect,
    #     extent=[
    #         fitsfile.hdul_dataset["time_axis"][0],
    #         fitsfile.hdul_dataset["time_axis"][-1000],
    #         fitsfile.hdul_dataset["frequency"][-1],
    #         fitsfile.hdul_dataset["frequency"][0],
    #     ],
    #     **kwargs
    # )

    # Follow the convention of inverting the Frequency axis
    # plt.gca().invert_yaxis()

    # Get the labels to use when plotting
    try:
        labels = LANGUAGES[language.lower()]
    except KeyError:
        # Defaults to English if an invalid or missing language is given.
        # Check languages.json for the currently supported languages.
        # Feel free to add a new language by adding it to languages.json
        # and then sending a Pull Request.
        labels = LANGUAGES["en"]

    # if show_colorbar:
    #     cb = plt.colorbar()
    #     cb.set_label(label=labels["colorbar"], fontsize=labels_fontsize)

    # plt.xlabel(labels["xlabel"], fontsize=labels_fontsize)
    # plt.ylabel(labels["ylabel"], fontsize=labels_fontsize)
    # plt.tick_params(labelsize=axis_params_labelsize)

    # Get the current figure to save it after showing it
    # fig = plt.gcf()

    # if show:
    #     plt.show()

    # filepath = None

    # if save:
    #     filepath = save_fits_figure(fitsfile, fig, ext)

    # # fig = plt.gcf()
    # plotly_fig = tls.mpl_to_plotly(fig)
    # plotly.io.show(plotly_fig)

    # return filepath
