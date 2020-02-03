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

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'pycallisto',
    'description': 'Python library for analyzing data from the e-Callisto '
                   'International Network of Solar Radio Spectrometers',
    'author': 'Andre Rossi Korol',
    'url': 'https://github.com/andrekorol/pycallisto',
    'download_url': 'https://github.com/andrekorol/pycallisto/archive/'
                    'master.zip',
    'author_email': 'anrobits@yahoo.com.br',
    'version': '0.1',
    'install_requires': ['numpy', 'astropy', 'matplotlib'],
    'packages': ['pycallisto']
}

setup(**config)
