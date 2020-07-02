import asyncio
import hashlib
import json
from cgi import parse_header
from os.path import join
from pathlib import Path
from typing import List, Optional, Sequence
from urllib.parse import unquote, urlparse

import aiofiles
import httpx
import numpy as np
from httpx import AsyncClient


async def download_file(
    url: str,
    client: Optional[AsyncClient] = AsyncClient(),
    filename: Optional[str] = "",
    folder: Optional[str] = "",
) -> Path:
    """Use an async `client` to download the file found at `url`
    and save it to `folder` as `filename`"""
    async with client.stream("GET", url) as resp:
        resp.raise_for_status()
        if not filename:
            params = {}
            if "Content-Disposition" in resp.headers:
                content_disposition = resp.headers.get("Content-Disposition")
                _, params = parse_header(content_disposition)
            if params and "filename*" in params:
                filename_str = params["filename*"]
                encoding, filename = filename_str.split("''")
                filename = unquote(filename, encoding)
            elif params and "filename" in params:
                filename = unquote(params["filename"])
            else:
                parsed_url = urlparse(url)
                filename = unquote(Path(parsed_url.path).name)

        async with aiofiles.open(join(folder, filename), "wb") as f:
            async for chunk in resp.aiter_bytes():
                if chunk:
                    await f.write(chunk)

    return Path(filename)


async def downloadfits(url_list: Sequence[str]) -> List[Path]:
    async with AsyncClient() as client:
        tasks = [download_file(url, client) for url in url_list]
        filenames = await asyncio.gather(*tasks)

        return sorted(filenames)


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


def get_test_file() -> Path:
    """Download a FITS file from e-Callisto to use during the tests.
    
    :returns: Path object of the downloaded FITS file.
    """
    callisto_archives = (
        "http://soleil80.cs.technik.fhnw.ch/" "solarradio/data/2002-20yy_Callisto/"
    )

    date_xpath = "2011/08/09/"
    fitsfile = "BLEN7M_20110809_080004_25.fit.gz"
    fitsurl = callisto_archives + date_xpath + fitsfile

    with open(fitsfile, "wb") as fin:
        with httpx.stream("GET", fitsurl) as r:
            for chunk in r.iter_raw():
                fin.write(chunk)

    return Path(fitsfile)


def get_test_file_list() -> List[Path]:
    """Download a list of FITS files from e-Callisto to use during tests.

    :returns: List of Path objects of the downloaded FITS files.
    """
    callisto_archives = (
        "http://soleil80.cs.technik.fhnw.ch/" "solarradio/data/2002-20yy_Callisto/"
    )
    date_xpath = "2011/02/16/"
    file_list = [
        "BLEN7M_20110216_133009_24.fit.gz",
        "BLEN7M_20110216_134510_24.fit.gz",
        "BLEN7M_20110216_140011_24.fit.gz",
        "BLEN7M_20110216_141512_24.fit.gz",
        "BLEN7M_20110216_143014_24.fit.gz",
        "BLEN7M_20110216_144515_24.fit.gz",
        "BLEN7M_20110216_150016_24.fit.gz",
        "BLEN7M_20110216_151517_24.fit.gz",
        "BLEN7M_20110216_153019_24.fit.gz",
    ]

    url_list = []
    for fitsfile in file_list:
        fitsurl = callisto_archives + date_xpath + fitsfile
        url_list.append(fitsurl)
    filepaths = asyncio.run(downloadfits(url_list))

    return filepaths
