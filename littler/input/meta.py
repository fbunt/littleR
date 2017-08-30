import datetime
import os
import re
import yaml

from littler.core import LittleRError
from littler.output import cli_out


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
    values in the files header. If all of the defaults are specified,
    the file will not be read from and the defaults will be returned.
    """

    defaults = [default_id, default_source, default_name, default_datetime]
    if None not in defaults:
        return defaults

    line = fd.readline()
    if not line.strip() == '---':
        cli_out.error('One or more meta data values were not specified and no header was found in the data file.')
        raise MetaDataParsingError('Could not find start of meta data header')

    lines = line
    # Use while loop instead of for in case read*() methods are called on
    # this file object later. 'for line in fd:' breaks those methods.
    while True:
        line = fd.readline()
        lines += line
        if line.startswith('...') or not line:
            break
    try:
        data = yaml.load(lines, Loader=yaml.BaseLoader)
    except yaml.YAMLError:
        cli_out.error('Failed while parsing data header.')
        raise MetaDataParsingError('Failed while attempting to parse meta data header')

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
        cli_out.error('Invalid header title(s).')
        raise MetaDataParsingError('Invalid header title(s)')
    if default_name is None:
        name = os.path.splitext(os.path.basename(fd.name))[0]
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
            cli_out.error('Could not parse date: ' + repr(datestr))
            raise MetaDataParsingError('Could not parse date: ' + repr(datestr))
    try:
        return datetime.date(int(match.group(3)), int(match.group(1)), int(match.group(2)))
    except ValueError:
        cli_out.error('Could not parse date: ' + repr(datestr))
        raise MetaDataParsingError('Could not parse date: ' + repr(datestr))


def _parse_time(timestr):
    h, m, s = timestr.strip().split(':')
    try:
        return datetime.time(int(h), int(m), int(s), 0, UTC())
    except ValueError:
        cli_out.error('Could not parse time: ' + repr(timestr))
        raise MetaDataParsingError('Could not parse time: ' + repr(timestr))


_ZERO = datetime.timedelta(0)


class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return _ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return _ZERO
