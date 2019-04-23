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

from urllib.error import HTTPError, URLError
import urllib.request
from os.path import join, abspath
from shutil import move
from socket import timeout


def download_from_url(url: str, save_dir: str = ''):
    """
    Downloads the file found at the given url.

    :param url: url string of a file to be downloaded.
    :param save_dir: directory to save downloaded file.
    If omitted, the file is saved in the current working directory.
    :returns: absolute path of file downloaded from the given url.
    """
    assert isinstance(url, str), "{} is not a string".format(url)
    assert isinstance(save_dir, str), "{} is not a string".format(save_dir)

    try:
        downloaded_file = urllib.request.urlretrieve(url, url.split('/')[-1])
        filename = downloaded_file[0]

        if save_dir != '':
            file_path = join(save_dir, filename)
            move(filename, file_path)
            urllib.request.urlcleanup()
            return abspath(file_path)

        urllib.request.urlcleanup()
        return abspath(filename)

    except (HTTPError, URLError) as error:
        urllib.request.urlcleanup()
        print("Data from {} not retrieved because {}".format(url, error))
    except ValueError:
        urllib.request.urlcleanup()
        print("unknown url type: '{}'".format(url))
        print(url, "is not a valid url")
    except timeout:
        urllib.request.urlcleanup()
        print("socket timed out - URL {}".format(url))
