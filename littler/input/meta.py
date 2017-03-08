import datetime
import os
import re
import yaml


class MetaDataParsingError(Exception):
    pass


def parse_meta_data(fd):
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
        id_ = data['id']
        source = data['source']
        date = _parse_date(data['date'])
        time = _parse_time(data['start time'])
    except KeyError:
        raise MetaDataParsingError('Invalid header title(s)')
    dt = datetime.datetime.combine(date, time)
    name = os.path.splitext(os.path.basename(fd.name))[0]
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
