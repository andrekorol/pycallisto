# FitsFile: Classes and methods for reading and plotting data from FITS files
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

import os
import fnmatch
import json
import itertools
from datetime import timedelta

from matplotlib import pyplot as plt
import numpy as np
from astropy.io import fits

from pycallisto.fitserror import FitsFileError


def digit_to_voltage(digits):
        return digits / 255.0 * 2500.0


class FitsFile(object):
    """Main entry point to the FITS file format."""
    def __init__(self, filename, filepath=""):
        self.filename = filename  # Name of the FITS file
        if filepath:
            self.filepath = filepath  # Path to the FITS file
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
                self.filepath = matches[0]
        try:
            self.hdul = fits.open(self.filepath)    # List of HDUs
            # (Header Data Unit)
        except OSError:
            error_message = f"{self.filename} is not a valid FITS file "
            error_message += "(e.g., .fits, .fit, .fit.gz, .fts)"
            raise FitsFileError(error_message)


class ECallistoFitsFile(FitsFile):
    def __init__(self, filename, filepath=""):
        FitsFile.__init__(self, filename, filepath)
        hdul_dataset = {}
        hdul = self.hdul

        hdul_dataset['data'] = hdul[0].data.astype(np.float32)
        hdul_dataset['v_min'] = -1  # -0.5, 100
        hdul_dataset['v_max'] = 8  # 4, 160
        hdul_dataset['dref'] = hdul_dataset['data'] - \
            np.min(hdul_dataset['data'])
        # conversion digit->voltage->into db
        hdul_dataset['db'] = digit_to_voltage(hdul_dataset['dref']) / 25.4
        hdul_dataset['db_median'] = np.median(hdul_dataset['db'], axis=1,
                                              keepdims=True)
        hdul_dataset['hh'] = float(hdul[0].header['TIME-OBS'].split(':')[0])
        hdul_dataset['mm'] = float(hdul[0].header['TIME-OBS'].split(':')[1])
        hdul_dataset['ss'] = float(hdul[0].header['TIME-OBS'].split(':')[2])
        hdul_dataset['time'] = hdul[1].data[0][0].astype(np.float32)
        hdul_dataset['f0'] = hdul[1].data[0][1].astype(np.float32)
        # cut lower 10 channels:
        hdul_dataset['frequency'] = hdul_dataset['f0'][:-10]
        hdul_dataset['start_time'] = hdul_dataset['hh'] * 3600 + \
            hdul_dataset['mm'] * 60 + hdul_dataset['ss']
        hdul_dataset['rows'] = hdul_dataset['data'].shape[0]
        hdul_dataset['columns'] = hdul_dataset['data'].shape[1]
        hdul_dataset['dt'] = hdul_dataset['time'][1] - hdul_dataset['time'][0]
        hdul_dataset['time_axis'] = (hdul_dataset['start_time'] +
                                     hdul_dataset['dt'] *
                                     np.arange(hdul_dataset['columns'])) / 3600
        hdul_dataset['freq_axis'] = np.linspace(hdul_dataset['frequency'][0],
                                                hdul_dataset['frequency'][-1],
                                                3600)
        self.hdul_dataset = hdul_dataset
        self.hdul.close()

    def plot_db_above_background(self, show=False, save=True):
        plt.figure(1, figsize=(11, 6))
        plt.imshow(self.hdul_dataset['db'] - self.hdul_dataset['db_median'],
                   cmap='magma', norm=plt.Normalize(self.hdul_dataset['v_min'],
                                                    self.hdul_dataset['v_max']
                                                    ),
                   aspect='auto', extent=[self.hdul_dataset['time_axis'][0],
                                          self.hdul_dataset['time_axis']
                                          [-1000],
                                          self.hdul_dataset['frequency'][-1],
                                          self.hdul_dataset['frequency'][0]])
        plt.gca().invert_yaxis()
        plt.colorbar(label='dB above background')
        plt.xlabel('Time (UT)', fontsize=15)
        plt.ylabel('Frequency (MHz)', fontsize=15)
        plt.title(self.filename, fontsize=16)
        plt.tick_params(labelsize=14)
        if save:
            img_filename = '.'.join(self.filepath.split('.')[:-2]) + '.png'
            plt.savefig(img_filename, bbox_inches='tight')
        if show:
            plt.show()
        plt.clf()
        plt.cla()
        plt.close('all')

    def plot_freq_range_db_above_background(self, start_freq, end_freq,
                                            show=False, save=True):
        plt.figure(1, figsize=(11, 6))
        plt.imshow(self.hdul_dataset['db'] - self.hdul_dataset['db_median'],
                   cmap='magma', norm=plt.Normalize(self.hdul_dataset['v_min'],
                                                    self.hdul_dataset['v_max']
                                                    ),
                   aspect='auto', extent=[self.hdul_dataset['time_axis'][0],
                                          self.hdul_dataset['time_axis']
                                          [-1000],
                                          self.hdul_dataset['frequency'][-1],
                                          self.hdul_dataset['frequency'][0]])
        plt.ylim(start_freq, end_freq)
        plt.gca().invert_yaxis()
        plt.colorbar(label='dB above background')
        plt.xlabel('Time (UT)', fontsize=15)
        plt.ylabel('Frequency (MHz)', fontsize=15)
        plt.title(self.filename, fontsize=16)
        plt.tick_params(labelsize=14)
        if save:
            img_filename = '.'.join(self.filepath.split('.')[:-2]) + '.png'
            plt.savefig(img_filename, bbox_inches='tight')
        if show:
            plt.show()
        plt.clf()
        plt.cla()
        plt.close('all')

    @staticmethod
    def plot_fits_files_list(files_list: list, title: str = None,
                             plot_filename: str = None, lang: str = 'en',
                             start_time: float = None, end_time: float = None,
                             start_freq: int = None, end_freq: int = None,
                             show: bool = False):

        extended_db = None
        ext_time_axis = None
        plt.figure(1, figsize=(11, 6))
        fitsfile = None

        for file in files_list:
            fits_filename = file.split(os.sep)[-1]

            fitsfile = ECallistoFitsFile(fits_filename)

            if extended_db is None and ext_time_axis is None:
                extended_db = fitsfile.hdul_dataset['db']
                ext_time_axis = fitsfile.hdul_dataset['time_axis']
            else:
                extended_db = np.hstack((extended_db,
                                         fitsfile.hdul_dataset['db']))
                ext_time_axis = np.hstack((ext_time_axis,
                                           fitsfile.hdul_dataset['time_axis']))
        extended_db_median = np.median(extended_db, axis=1, keepdims=True)
        plt.imshow(extended_db - extended_db_median, cmap='magma',
                   norm=plt.Normalize(fitsfile.hdul_dataset['v_min'],
                                      fitsfile.hdul_dataset['v_max']),
                   aspect='auto',
                   extent=[ext_time_axis[0],
                           ext_time_axis[-1],
                           fitsfile.hdul_dataset['frequency'][-1],
                           fitsfile.hdul_dataset['frequency'][0]])

        if start_freq is not None or end_freq is not None:
            plt.ylim(start_freq, end_freq)

        if start_time is not None or end_time is not None:
            plt.xlim(start_time, end_time)

        plt.gca().invert_yaxis()

        #  hours_delta = round(ext_time_axis[-1], 2) -
        #  round(ext_time_axis[0], 2)
        #  minutes_delta = hours_delta * 60
        #  ticks_interval = minutes_delta / len(locs)
        #  print(ticks_interval)
        #  exit(0)
        #  hours_xticks = []
        #  hour = timedelta(hours=round(ext_time_axis[0], 2))
        #  hours_xticks.append(':'.join(hour.__str__().split(':')[:-1]))
        #  while hour != timedelta(hours=round(ext_time_axis[-1], 2)):
        #      hour = hour + timedelta(minutes=ticks_interval)
        #      hours_xticks.append(':'.join(hour.__str__().split(':')[:-1]))
        #
        #  plt.xticks(np.arange(len(hours_xticks)), hours_xticks)
        labels = {
            'en': {'colorbar': 'dB above background',
                   'xlabel': 'Time (UT)',
                   'ylabel': 'Frequency (MHz)'},

            'pt': {'colorbar': 'dB acima da frequência de fundo',
                   'xlabel': 'Tempo (UT)',
                   'ylabel': 'Frequência (MHz)'}
        }[lang]

        plt.colorbar(label=labels['colorbar'])
        plt.xlabel(labels['xlabel'], fontsize=15)
        plt.ylabel(labels['ylabel'], fontsize=15)
        plt.tick_params(labelsize=14)

        hours_xticks = []
        locs, _ = plt.xticks()
        for loc in locs:
            hour = str(int(loc)) + ':' + str(int((loc - int(loc)) * 60))
            if hour.split(':')[-1] == '0':
                hour += '0'
            if len(hour.split(':')[-1]) == 1:
                hour = hour.split(':')[0] + ":0" + hour.split(':')[-1]
            hours_xticks.append(hour)

        #  print(locs)
        #  print(hours_xticks)
        #  hours_xticks.pop()

        initial_hour = timedelta(hours=round(ext_time_axis[0], 2))

        print(':'.join(str(initial_hour).split(':')[:-1]), hours_xticks[0])
        initial_seconds = initial_hour.seconds
        initial_xticks_seconds = int(hours_xticks[0].split(':')[0]) * 3600
        initial_xticks_seconds += int(hours_xticks[0].split(':')[-1]) * 60

        if initial_seconds != initial_xticks_seconds:
            hours_xticks.pop(0)
            locs = locs[1:]

        print("initial_seconds =", initial_seconds)
        print("initial_xticks_seconds =", initial_xticks_seconds)
        for index, item in enumerate(hours_xticks):
            if len(item.split(':')[0]) == 1:
                hours_xticks[index] = '0' + item

        # TODO: Fix line below to only remove item if last hour is greater
        # than last hour in FITS file
        # final_hour = extended_time_axis[-1]...
        final_hour = timedelta(hours=round(ext_time_axis[-1], 2))
        final_seconds = final_hour.seconds
        final_xticks_seconds = int(hours_xticks[-1].split(':')[0]) * 3600
        final_xticks_seconds += int(hours_xticks[-1].split(':')[-1]) * 60

        if final_seconds != final_xticks_seconds:
            hours_xticks.pop()
            #  plt.xticks(locs[:-1], hours_xticks)
            locs = locs[:-1]
        #  else:
        #      plt.xticks(locs, hours_xticks)

        if initial_xticks_seconds != initial_seconds:
            print("type =", type(hours_xticks[0]))
            last_minutes = int(hours_xticks[-1].split(':')[0]) * 60
            last_minutes += int(hours_xticks[-1].split(':')[-1])
            first_minutes = int(hours_xticks[0].split(':')[0]) * 60
            first_minutes += int(hours_xticks[0].split(':')[-1])
            minutes_delta = last_minutes - first_minutes
            print("minutes_delta =", minutes_delta)
            ticks_interval = int(round(minutes_delta / (len(locs) - 1), 0))
            print("ticks_interval =", ticks_interval)
            final_xticks = []
            hour = timedelta(minutes=first_minutes)
            final_xticks.append(':'.join(hour.__str__().split(':')[:-1]))

            for _ in itertools.repeat(None, len(locs) - 1):
                hour = hour + timedelta(minutes=ticks_interval)
                final_xticks.append(':'.join(hour.__str__().split(':')[:-1]))

            plt.xticks(locs, final_xticks)

        else:
            hours_delta = round(ext_time_axis[-1], 2)
            hours_delta -= round(ext_time_axis[0], 2)
            minutes_delta = hours_delta * 60
            ticks_interval = int(round(minutes_delta / (len(locs) - 1), 0))
            print("ticks_interval =", ticks_interval)
            final_xticks = []
            hour = initial_hour
            final_xticks.append(':'.join(hour.__str__().split(':')[:-1]))

            for _ in itertools.repeat(None, len(locs) - 1):
                hour = hour + timedelta(minutes=ticks_interval)
                final_xticks.append(':'.join(hour.__str__().split(':')[:-1]))

            print("final_xticks =", final_xticks)
            plt.xticks(locs, final_xticks)

        #  print("final_seconds =", final_seconds)
        #  print("final_xticks_seconds =", final_xticks_seconds)
        final_hour_str = final_hour.__str__()
        if len(final_hour_str.split(':')[0]) == 1:
            final_hour_str = '0' + final_hour_str
        if title is None:
            # Define plot's title
            title_start = '_'.join(files_list[0].split('_')[:-1])
            freq_band = files_list[-1].split('_')[-1].split('.')[0]
            title_end = ''.join(final_hour_str.split(':'))
            title_end = '_'.join([title_end, freq_band])
            title = '_'.join([title_start, title_end])
            print(title)
        plt.title(title, fontsize=16)

        if plot_filename is None:
            plot_filename = title

        plt.savefig(os.path.join(os.getcwd(), plot_filename) + '.png',
                    bbox_inches='tight')

        if show:
            plt.show()

        plt.clf()
        plt.cla()
        plt.close('all')

    @staticmethod
    def plot_json_fits_file(filename):
        with open(filename) as json_file:
            json_str = json_file.read()
            json_data = json.loads(json_str)
        for fits_list in json_data:
            ECallistoFitsFile.plot_fits_files_list(fits_list)

    def set_fits_linear_regression(self):
        hdul_dataset = self.hdul_dataset
        hdul_dataset['lin_reg'] = np.polyfit(hdul_dataset['time_axis'],
                                             hdul_dataset['freq_axis'],
                                             1)

    def get_fits_linear_regression(self):
        return self.hdul_dataset['lin_reg']

    def set_fits_linear_regression_function(self):
        hdul_dataset = self.hdul_dataset
        hdul_dataset['lin_reg_fn'] = np.poly1d(hdul_dataset['lin_reg'])

    def get_fits_linear_regression_function(self):
        return self.hdul_dataset['lin_reg_fn']

    @staticmethod
    def fits_list_linear_regression(file_list):
        """Apply linear regression on extended time and frequency axis"""
        extended_time = None
        extended_freq = None

        for name in file_list:
            filename = name.split(os.sep)[-1]

            fitsfile = ECallistoFitsFile(filename)
            dataset = fitsfile.hdul_dataset

            if extended_time is None and extended_freq is None:
                extended_time = dataset['time_axis']
                extended_freq = dataset['freq_axis']
            else:
                extended_time = np.hstack((extended_time,
                                           dataset['time_axis']))
                extended_freq = np.hstack((extended_freq,
                                           dataset['freq_axis']))
        lin_reg = np.polyfit(extended_time, extended_freq, 1)
        lin_reg_fn = np.poly1d(lin_reg)

        return lin_reg_fn

    def plot_fits_linear_regression(self, show=False, save=True):
        hdul_dataset = self.hdul_dataset
        plt.gca().invert_yaxis()
        plt.plot(hdul_dataset['time'][2000:],
                 hdul_dataset['freq_axis'][2000:],
                 hdul_dataset['time'][2000:],
                 hdul_dataset['lin_reg_fn'](hdul_dataset['time'][2000:]),
                 'r')
        plt.xlabel('Time (UT)', fontsize=15)
        plt.ylabel('Frequency (MHz)', fontsize=15)
        slope = hdul_dataset['lin_reg'][0]
        intercept = hdul_dataset['lin_reg'][1]
        plt.title(self.filename + ' Simple Linear Regression\nf(t) = ' +
                  f'{intercept:.2f} + ({slope:.2f}t)', fontsize=16)
        plt.tick_params(labelsize=14)
        if save:
            img_filename = '.'.join(self.filepath.split('.')[:-2]) +\
                           'linear_regression.png'
            plt.savefig(img_filename, bbox_inches='tight')
        if show:
            plt.show()
        # TODO: Fix the plot_fits_linear_regression method
