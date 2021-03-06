# from io import open as iopen

from littler.config import get_parser
from littler.core import run_core, NoDataError
from littler.adapters import get_adapter
from littler.input.meta import parse_meta_data, MetaDataParsingError
from littler.output import cli_out


def _compose_meta_data(fd, user_id, user_source, user_name, user_datetime):
    """Parse meta data from file or use user data if provided"""
    if None not in [user_id, user_source, user_name, user_datetime]:
        return user_id, user_source, user_name, user_datetime
    return parse_meta_data(fd, user_id, user_source, user_name, user_datetime)


def run():
    """Convert the input data file to LITTLE_R output."""
    args = get_parser().parse_args()
    # with iopen(args.file, encoding=args.encoding) as data_fd:
    with open(args.file) as data_fd:
        try:
            meta = _compose_meta_data(data_fd, args.id, args.source, args.name, args.date_time_string)
        except MetaDataParsingError:
            cli_out.info('Failed while gathering meta data. Exiting...')
            return 1
        adapter = get_adapter(args.type, data_fd, *meta)
    fout = open(args.outfile, 'w')
    try:
        return run_core(adapter, fout)
    except NoDataError:
        cli_out.info('No data. Exiting...')
        return 1


main = run
