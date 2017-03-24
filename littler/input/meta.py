import datetime
import os
import re
import yaml

from littler.core import LittleRError


class MetaDataParsingError(LittleRError):
    pass


_ID_KEY = 'id'
_SOURCE_KEY = 'source'
_DATE_KEY = 'date'
_START_TIME_KEY = 'start time'


def parse_meta_data(fd, default_id=None, default_source=None,
                    default_name=None, default_datetime=None):
    """Parse the meta information for the data from the file

    If the defaults are specified, they will override the corresponding
    values in the files header.
    """
    line = fd.readline()
    if not line.strip() == '---':
        raise MetaDataParsingError('Could not find meta data')

    lines = line
    for line in fd:
        lines += line
        if line.startswith('...'):
            break
    try:
        data = yaml.load(lines, Loader=yaml.BaseLoader)
    except yaml.YAMLError:
        raise MetaDataParsingError('Failed while attempting to parse meta data')

    try:
        id_ = default_id if default_id is not None else data[_ID_KEY]
        source = default_source if default_id is not None else data[_SOURCE_KEY]
        if default_datetime is None:
            date = _parse_date(data[_DATE_KEY])
            time = _parse_time(data[_START_TIME_KEY])
            dt = datetime.datetime.combine(date, time)
        else:
            dt = default_datetime
    except KeyError:
        raise MetaDataParsingError('Invalid header title(s)')
    if default_name is None:
        name = name = os.path.splitext(os.path.basename(fd.name))[0]
    else:
        name = default_name
    return id_, source, name, dt


def _parse_date(datestr):
    pat = re.compile('(\d+)[:|/|-](\d+)[:|/|-](\d+)')
    mat = pat.match(datestr)
    match = None
    if mat:
        match = mat
    else:
        pat = re.compile('(\d{2})(\d{2})(\d{4})')
        mat = pat.match(datestr)
        if mat:
            match = mat
        else:
            raise MetaDataParsingError('Could not parse date: ' + repr(datestr))
    try:
        return datetime.date(int(match.group(3)), int(match.group(1)), int(match.group(2)))
    except ValueError:
        raise MetaDataParsingError('Could not parse date: ' + repr(datestr))


def _parse_time(timestr):
    h, m, s = timestr.strip().split(':')
    try:
        return datetime.time(int(h), int(m), int(s), 0, _UTC())
    except ValueError:
        raise MetaDataParsingError('Could not parse time: ' + repr(timestr))


_ZERO = datetime.timedelta(0)


class _UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return _ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return _ZERO
