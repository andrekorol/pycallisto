from matplotlib import pyplot as plt
from datetime import timedelta
import numpy as np
from astropy.io import fits
import os
from tkinter import Tk
from tkinter import messagebox
from tkinter import filedialog
import math


class FitsFile(object):
    """Main entry point to the FITS file format"""
    def __init__(self, filename: str = None):
        self.filename = filename
        self.hdul = None
        self.file_path = None

    def set_filename(self, filename):
        self.filename = filename

    def get_filename(self):
        return self.filename

    def set_file_path(self, file_path: str = None):
        if file_path is not None:
            self.file_path = file_path
        else:
            root = Tk()
            root.withdraw()
            if self.filename is not None:
                try:
                    top = os.getcwd()
                    for root, dirs, files in os.walk(top):
                        for file in files:
                            if file == self.filename:
                                self.file_path = os.path.abspath(file)
                finally:
                    if self.file_path is None:
                        messagebox.showerror('FileNotFoundError: [Errno 2]',
                                             'No such file or directory: '
                                             f'{self.filename}')
                        raise FileNotFoundError

            else:
                self.file_path = filedialog.askopenfilename()
                self.set_filename(self.file_path.split('/')[-1])

    def get_file_path(self):
        return self.file_path

    def set_hdul(self):
        try:
            self.hdul = fits.open(self.file_path)
        except FileNotFoundError as e:
            messagebox.showerror('FileNotFoundError: [Errno 2]',
                                 'No such file or directory: '
                                 f'{self.file_path}')
            raise e
        except OSError as e:
            messagebox.showerror('OSError',
                                 f'{self.file_path} is not a FITS file.')
            raise e

    def get_hdul(self):
        return self.hdul

    def close_hdul(self):
        self.hdul.close()

    def delete_file(self):
        os.remove(self.file_path)


class ECallistoFitsFile(FitsFile):
    def __init__(self, filename: str = None):
        FitsFile.__init__(self, filename)
        self.hdul_dataset = {}

    @staticmethod
    def digit_to_voltage(digits):
        return digits / 255.0 * 2500.0

    def set_hdul_dataset(self):
        if self.hdul is None:
            if self.file_path is None:
                self.set_file_path()
            self.set_hdul()
        hdul_dataset = self.hdul_dataset
        hdul = self.hdul

        hdul_dataset['data'] = hdul[0].data.astype(np.float32)
        hdul_dataset['v_min'] = -1  # -0.5, 100
        hdul_dataset['v_max'] = 8  # 4, 160
        hdul_dataset['dref'] = hdul_dataset['data'] - \
                               np.min(hdul_dataset['data'])
        # conversion digit->voltage->into db
        hdul_dataset['db'] = self.digit_to_voltage(hdul_dataset['dref']) / 25.4
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
        hdul_dataset['time_axis'] = (hdul_dataset['start_time']
                                     + hdul_dataset['dt'] *
                                     np.arange(hdul_dataset['columns'])) / 3600
        hdul_dataset['freq_axis'] = np.linspace(hdul_dataset['frequency'][0],
                                                hdul_dataset['frequency'][-1],
                                                3600)
        self.close_hdul()

    def get_hdul_dataset(self):
        return self.hdul_dataset

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
            img_filename = '.'.join(self.file_path.split('.')[:-2]) + '.png'
            plt.savefig(img_filename, bbox_inches='tight')
        if show:
            plt.show()
        plt.clf()
        plt.cla()
        plt.close('all')

    def plot_freq_range_db_above_background(self, start_freq, end_freq, show=False,
                                            save=True):
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
            img_filename = '.'.join(self.file_path.split('.')[:-2]) + '.png'
            plt.savefig(img_filename, bbox_inches='tight')
        if show:
            plt.show()
        plt.clf()
        plt.cla()
        plt.close('all')

    @staticmethod
    def plot_fits_files_list(files_list: list, start_freq: int, end_freq: int,
                             title: str, lang: str, plot_filename: str):
        extended_db = None
        ext_time_axis = None
        plt.figure(1, figsize=(11, 6))
        fitsfile = None
        for file in files_list:
            fits_filename = file.split(os.sep)[-1]
            fitsfile = ECallistoFitsFile(fits_filename)
            fitsfile.set_file_path()
            fitsfile.set_hdul_dataset()
            if extended_db is None and ext_time_axis is None:
                extended_db = fitsfile.hdul_dataset['db']
                ext_time_axis = fitsfile.hdul_dataset['time_axis']
            else:
                extended_db = np.hstack((extended_db,
                                         fitsfile.hdul_dataset['db']))
                ext_time_axis = np.hstack((ext_time_axis,
                                           fitsfile.hdul_dataset['time_axis']))
            fitsfile.delete_file()
        extended_db_median = np.median(extended_db, axis=1, keepdims=True)
        plt.imshow(extended_db - extended_db_median, cmap='magma',
                   norm=plt.Normalize(fitsfile.hdul_dataset['v_min'],
                                      fitsfile.hdul_dataset['v_max']),
                   aspect='auto',
                   extent=[ext_time_axis[0],
                           ext_time_axis[-1],
                           fitsfile.hdul_dataset['frequency'][-1],
                           fitsfile.hdul_dataset['frequency'][0]])
        plt.ylim(start_freq, end_freq)
        plt.gca().invert_yaxis()

        hours_delta = round(ext_time_axis[-1], 2) - round(ext_time_axis[0], 2)
        minutes_delta = hours_delta * 60
        ticks_interval = minutes_delta / 8
        hours_xticks = []
        hour = timedelta(hours=round(ext_time_axis[0], 2))
        hours_xticks.append(':'.join(hour.__str__().split(':')[:-1]))
        while hour != timedelta(hours=round(ext_time_axis[-1], 2)):
            hour = hour + timedelta(minutes=ticks_interval)
            hours_xticks.append(':'.join(hour.__str__().split(':')[:-1]))

        plt.gca().set_xticklabels(hours_xticks, fontsize=15)

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
        plt.title(title, fontsize=16)
        plt.tick_params(labelsize=14)

        plt.savefig(os.path.join(os.getcwd(), plot_filename) + '.png',
                    bbox_inches='tight')
        plt.show()

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
            img_filename = '.'.join(self.file_path.split('.')[:-2]) +\
                           'linear_regression.png'
            plt.savefig(img_filename, bbox_inches='tight')
        if show:
            plt.show()
        # TODO: Fix the plot_fits_linear_regression method


class ChromosphericEvaporationFitsFile(ECallistoFitsFile):
    def __init__(self, filename: str = None):
        ECallistoFitsFile.__init__(self, filename)
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
