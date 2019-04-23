try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'pycallisto',
    'description': 'Python tools for analyzing data from the e-Callisto '
                   'International Network of Solar Radio Spectrometers',
    'author': 'Andre Rossi Korol',
    'url': 'https://github.com/andrekorol/pycallisto',
    'download_url': 'https://github.com/andrekorol/pycallisto/archive/'
                    'master.zip',
    'author_email': 'anrobits@yahoo.com.br',
    'version': '0.1',
    'install_requires': ['numpy', 'astropy', 'matplotlib'],
}

setup(**config)
