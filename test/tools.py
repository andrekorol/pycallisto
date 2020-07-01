import hashlib
import json

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
