import numpy as np
import pandas as pd

from .adapter import InputAdapter, Level


_NUM_COLS = 16
# Time (sec): seconds after start
_ITIME = 0
# Pressure (mB)
_IPRES = 1
# Temperature (C)
_ITEMP = 2
# Relative Humidity (%)
_IRH = 3
# Wind Speed (m/s)
_IWS = 4
# Wind Direction (degrees)
_IWD = 5
# Latitude (degrees)
_ILAT = 6
# Longitude (degrees)
_ILON = 7
# Altitude (m)
# TODO: add note on why this is different from elevation
_IALT = 8
# Geopotential (m)
_IGPOT = 9
# Dew point (C)
_IDEW = 10
# Virtual Temperature (C)
_IVTEMP = 11
# Elevation (degrees WTF?)
# TODO: figure out what is going on with units
_IELE = 12
# Azimuth (degrees)
_IAZI = 13
# Range (m) TODO: what is this?
_IRANGE = 14
# D (kg/m3) TODO: what is this?
_ID = 15


class GrawAdapter(InputAdapter):
    def __init__(self, src=None):
        super().__init__()
        if src is not None:
            self._parse(src)

    def _parse(self, src):
        pass
