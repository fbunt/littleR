import argparse
import datetime
import os
import re

from littler.adapters import adapters_map
from littler.core import LittleRError


class ConfigError(LittleRError):
    pass


def get_parser():
    lrparser = argparse.ArgumentParser(
        prog='littler',
        description='A program for converting various data formats to the '
                    'LITTLE_R format.')
    lrparser.add_argument(
        'file',
        help='The file to be converted to LITTLE_R',
        type=_validate_file_name)
    # TODO: let user supply adapter
    # lrparser.add_argument(
    #     '--encoding',
    #     help='Special encoding to use for file',
    #     default='utf-8')
    lrparser.add_argument(
        '-n', '--name',
        help='Name of the data set')
    lrparser.add_argument(
        '-i', '--id',
        help='ID of the data set')
    lrparser.add_argument(
        '-d', '--date_time_string',
        help='String representing the date and (start) time of the data. Has '
             'the form \'MMDDYYYYhhmmss\'',
        type=_parse_datestr)
    lrparser.add_argument(
        '-s', '--source',
        help='Name of of the data\'s source. If this includes spaces, use '
             'quotes.')
    lrparser.add_argument(
        '-o', '--outfile',
        help='Name of the output file',
        default='littler.out',
        type=_check_outfile)
    lrparser.add_argument(
        '-t', '--type',
        help='The type of the file to be converted (e.g. graw)',
        required=True,
        type=_validate_type)
    return lrparser


def _validate_file_name(fname):
    if os.path.isfile(fname):
        return fname
    raise ConfigError('Could not find file: ' + fname)


def _validate_type(t):
    t = t.lower()
    if t in adapters_map:
        return t
    raise ConfigError('Unknown data type: ' + t)


def _check_outfile(fname):
    if os.path.isfile(fname):
        raise ConfigError('Output file name already exists: ' + fname)
    return str(fname)


def _parse_datestr(s):
    if s is None:
        return None
    # 'MMDDYYYYhhmmss'
    p = re.compile('^(\d{2})(\d{2})(\d{4})(\d{2})(\d{2})(\d{2})$')
    m = p.match(s)
    if not m:
        raise ConfigError('Invalid date-time string: ' + s)
    from littler.input.meta import UTC
    month = m.group(1)
    day = m.group(2)
    year = m.group(3)
    hour = m.group(4)
    minute = m.group(5)
    sec = m.group(6)
    return datetime.datetime(year, month, day, hour, minute, sec, tzinfo=UTC())
