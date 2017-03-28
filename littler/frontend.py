from io import open as iopen

from littler.config import get_parser
from littler.core import run_core
from littler.adapters import adapters
from littler.input.meta import parse_meta_data


def _compose_meta_data(fd, user_id, user_source, user_name, user_datetime):
    """Parse meta data from file or use user data if provided"""
    if None not in [user_id, user_source, user_name, user_datetime]:
        return user_id, user_source, user_name, user_datetime
    return parse_meta_data(fd, user_id, user_source, user_name, user_datetime)


def run():
    args = get_parser().parse_args()
    fd = iopen(args.file, encoding=args.encoding)
    id_, source, name, dt = _compose_meta_data(fd, args.id, args.source, args.name, args.date_time_string)
    adapter = adapters[args.type](fd, src_start_datetime=dt, name=name, src_id=id_, source=source)
    fout = open(args.outfile, 'w')
    run_core(adapter, fout)
