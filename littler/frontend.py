import argparse
import datetime
from io import open as iopen
import os

from littler.core import LittleRError, run_core
from littler.adapters import adapters
from littler.input import parse_meta_data


class LittleRInputError(LittleRError):
    pass


def _validate_file_name(fname):
    if os.path.isfile(fname):
        return fname
    else:
        raise LittleRInputError('Could not find file: ' + fname)


def _validate_type(t):
    if t in adapters:
        return t
    raise LittleRInputError('Unknown data type: ' + t)


def _parse_datestr(s):
    if s is None:
        return None
    if len(s) != len('MMDDYYYYhhmmss'):
        raise LittleRInputError('Invalid date-time string: ' + s)
    from littler.input.meta import UTC
    month = int(s[:2])
    day = int(s[2:4])
    year = int(s[4:8])
    hour = int(s[8:10])
    minute = int(s[10:12])
    sec = int(s[12:])
    return datetime.datetime(year, month, day, hour, minute, sec, tzinfo=UTC())


def _compose_meta_data(fd, user_id, user_source, user_name, user_date_str):
    user_datetime = _parse_datestr(user_date_str)
    if None not in [user_id, user_source, user_name, user_datetime]:
        return user_id, user_source, user_name, user_datetime
    return parse_meta_data(fd, user_id, user_source, user_name, user_datetime)


# TODO: add full doc
lrparser = argparse.ArgumentParser(prog='littler',
                                   description='A program for converting various data formats to the LITTLE_R format.')
lrparser.add_argument('file',  help='The file to be converted to LITTLE_R', type=_validate_file_name)
# TODO: let user supply adapter
lrparser.add_argument('--encoding', help='Special encoding to use for file', default='utf-8')
lrparser.add_argument('-n', '--name', help='Name of the data set')
lrparser.add_argument('-i', '--id', help='ID of the data set')
lrparser.add_argument('-d', '--date_time_string',
                      help='String representing the date and (start) time of the data. Has the form \'MMDDYYYYhhmmss\'',
                      type=_parse_datestr)
lrparser.add_argument('-s', '--source', help='Name of of the data\'s source. If this includes spaces, use quotes.')
lrparser.add_argument('-t', '--type', help='The type of the file to be converted (e.g. graw)', required=True,
                      type=_validate_type)
args = lrparser.parse_args()
# TODO: reorganize
fd = iopen(args.file, encoding=args.encoding)
id_, source, name, dt = _compose_meta_data(fd, args.id, args.source, args.name, args.date_time_string)
adapter = adapters[args.type](fd, src_start_datetime=dt, name=name, src_id=id_, source=source)
fout = open('littler.out', 'w')
core = Core(adapter, fout)
core.run()
