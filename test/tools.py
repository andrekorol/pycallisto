import hashlib
import json

import httpx
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.float32):
            return str(obj)


def sha3_512(fname: str, block_size: int = 32768) -> str:
    """Get the SHA3-512 checksum of a given file.

    :param fname: name of the file to be checked.
    :param block_size: size, in bytes, of file chunks to be read
    at a time.
    :returns: hex string representation for the SHA3-512 hash digest.
    """
    with open(fname, "rb") as f:
        file_hash = hashlib.sha3_512()
        while chunk := f.read(block_size):
            file_hash.update(chunk)

    return file_hash.hexdigest()


def get_test_file():
    """Download a FITS file from e-Callisto to use during the tests."""
    test_file = "BLEN7M_20110809_080004_25.fit.gz"
    callisto_archives = (
        "http://soleil80.cs.technik.fhnw.ch/" "solarradio/data/2002-20yy_Callisto/"
    )

    date_xpath = "2011/08/09/"
    fitsfile = "BLEN7M_20110809_080004_25.fit.gz"
    fitsurl = callisto_archives + date_xpath + fitsfile

    with open(test_file, "wb") as fin:
        with httpx.stream("GET", fitsurl) as r:
            for chunk in r.iter_raw():
                fin.write(chunk)

    return test_file
