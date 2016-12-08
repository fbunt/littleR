import pandas as pd
import time

from littler.input.adapters.adapter import InputAdapter
from littler.input.level import Level

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
# Elevation (degrees)
# TODO: figure out what is going on with units
_IELE = 12
# Azimuth (degrees)
_IAZI = 13
# Range (m) TODO: what is this?
_IRANGE = 14
# D (kg/m3) TODO: what is this?
_ID = 15


class GrawAdapter(InputAdapter):
    def __init__(self, src, src_start_datetime=None):
        super().__init__()
        self.levels = []
        # TODO: use epoch?
        self._start_date = src_start_datetime or time.gmtime(0)
        self._parse(src)

    def getlevel(self, pos):
        return self.levels[pos]

    def _parse(self, src):
        data = pd.read_table(src, names=range(_NUM_COLS), skiprows=3, skipfooter=10, engine='python')
        self.count = data.shape[0]
        for i in range(self.count):
            level = Level()
            lv = data.iloc[i]
            level.lat = lv.loc[_ILAT]
            level.lon = lv.loc[_ILON]
            # TODO: implement id, name
            # TODO: confirm this is correct
            level.platform = 'FM-37 TEMP DROP'
            level.alt = lv.loc[_ILAT]
            # TODO: implement seq num
            level.date = _get_date_str(self._start_date, lv.loc[_ITIME])
            # TODO: implement SLP

            level.pres = (lv.loc[_IPRES], 0)
            level.height = (_convert_pres(lv.loc[_IALT]), 0)
            level.temp = (_convert_temp(lv.loc[_ITEMP]), 0)
            level.dewpoint = (_convert_temp(lv.loc[_IDEW]), 0)
            level.windspd = (lv.loc[_IWS], 0)
            level.winddir = (lv.loc[_IWD], 0)
            # TODO: implement wind u/v
            level.rh = (lv.loc[_IRH], 0)
            self.levels.append(level)


def _get_date_str(date, secs):
    # TODO: implement
    return ''


def _convert_pres(p_mb):
    return p_mb * 100.0


def _convert_temp(t_c):
    return t_c + 273.15
