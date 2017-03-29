import datetime
import pandas as pd
import re

from littler.adapters.adapter import InputAdapter
from littler.core import LittleRError
from littler.level import Level
from littler.utils import uv_from_met


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
_IALT = 8
# Dew point (C)
_IDEW = 9


class GrawParsingError(LittleRError):
    pass


class GrawAdapter(InputAdapter):
    def __init__(self, src, src_start_datetime, name='', src_id='', source=''):
        """
        :param src: The data source file or file name. Ownership is NOT assumed for open file objects.
        :param src_start_datetime: datetime.datetime The start data and time of the measurements
        """
        super(GrawAdapter, self).__init__()
        self.levels = []
        self._start_date = src_start_datetime
        self._src_name = name
        self._src_id = src_id
        self._src_source = source
        self._parse(src)

    def getlevel(self, pos):
        return self.levels[pos]

    def _parse(self, src):
        try:
            data = _parse_graw_file(src)
        except GrawParsingError as e:
            raise GrawParsingError("Could not parse graw data file: " + e.message)

        self.count = data.shape[0]
        for i in range(self.count):
            level = Level()
            lv = data.iloc[i]
            # Header
            level.lat = lv.loc[_ILAT]
            level.lon = lv.loc[_ILON]
            level.id = self._src_id
            level.name = self._src_name
            level.source = self._src_source
            level.platform = 'FM-38 TEMP MOBIL'
            level.alt = lv.loc[_IALT]
            # TODO: implement seq num
            level.is_sounding = True
            level.bogus = False
            level.date = _get_date_str(self._start_date, lv.loc[_ITIME])
            # TODO: implement SLP, sfc_pres

            # Fields
            level.pres = (_convert_pres(lv.loc[_IPRES]), 0)
            level.height = (lv.loc[_IALT], 0)
            level.temp = (_convert_temp(lv.loc[_ITEMP]), 0)
            level.dewpoint = (_convert_temp(lv.loc[_IDEW]), 0)
            wspd = lv.loc[_IWS]
            wdir = lv.loc[_IWD]
            level.windspd = (wspd, 0)
            level.winddir = (wdir, 0)
            u, v = uv_from_met(wspd, wdir)
            level.windu = (u, 0)
            level.windv = (v, 0)
            level.rh = (lv.loc[_IRH], 0)

            level.valid_fields = 9
            self.levels.append(level)


def _get_date_str(date, secs):
    t = date + datetime.timedelta(seconds=secs)
    # YYYYMMDDhhmmss
    return t.strftime('%Y%M%d%H%m%S')


def _convert_pres(p_mb):
    return p_mb * 100.0


def _convert_temp(t_c):
    return t_c + 273.15


# Data column labels
_LABEL_TIME = 'Time'
_LABEL_PRESS = 'P'
_LABEL_TEMP = 'T'
_LABEL_RH = 'Hu'
_LABEL_WS = 'Ws'
_LABEL_Wd = 'Wd'
_LABEL_LONG = 'Long.'
_LABEL_LAT = 'Lat.'
_LABEL_ALT = 'Alt'
_LABEL_DEW = 'Dewp.'
# These should have the same index as the corresponding index constant above.
_LABELS = [
    _LABEL_TIME, _LABEL_PRESS, _LABEL_TEMP, _LABEL_RH, _LABEL_WS,
    _LABEL_Wd, _LABEL_LONG, _LABEL_LAT, _LABEL_ALT, _LABEL_DEW
]

_DATA_INDICATOR = 'Profile Data:'


def _remove_graw_header(fd):
    while True:
        line = fd.readline()
        if line.startswith(_DATA_INDICATOR):
            return True
        if not line:
            break
    return False


def _parse_column_labels(fd):
    """Find the desired columns and return their indices"""
    cols = []
    line = fd.readline().strip()
    # Don't split on single spaces so multi word column labels are preserved (e.g. 'Virt. Temp')
    col_labels = re.split('[\t\n\r\f\v]+|[\s]{2,}', line)
    for label in _LABELS:
        try:
            cols.append(col_labels.index(label))
        except ValueError:
            raise GrawParsingError("Could not identify data columns")
    return cols


def _parse_graw_file(fd):
    if not _remove_graw_header(fd):
        raise GrawParsingError("Could not find profile data")
    cols = _parse_column_labels(fd)
    converters = {_ITIME: int}
    return pd.read_table(fd, names=range(len(_LABELS)), usecols=cols, skiprows=1,
                         skipfooter=10, converters=converters, engine='python')
