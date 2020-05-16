try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="pycallisto",
    description="Python library for analyzing data from the e-Callisto "
    "International Network of Solar Radio Spectrometers",
    author="Andre Rossi Korol",
    url="https=//github.com/andrekorol/pycallisto",
    download_url="https=//github.com/andrekorol/pycallisto/archive/master.zip",
    author_email="anrobits@yahoo.com.br",
    version="0.1.0",
    install_requires=["numpy", "astropy", "matplotlib"],
    packages=["pycallisto"],
)
