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
