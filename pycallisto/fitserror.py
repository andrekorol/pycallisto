class FitsFileError(Exception):
    """Exception to be raised when astropy.io.fits.open throws an OSError"""

    def __init__(self, message):
        super().__init__(message)
