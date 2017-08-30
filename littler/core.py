from littler.output import LittleRFormatter, cli_out


class LittleRError(Exception):
    pass


class NoDataError(LittleRError):
    pass


def run_core(adapter, fdout):
    """Write all levels from the source to the output in LITTLE_R format"""
    if adapter.count <= 0:
        cli_out.error('No data found. Level count: ' + str(adapter.count))
        raise NoDataError('No data found. Level count: ' + str(adapter.count))

    fmtr = LittleRFormatter()
    curlv = adapter.getlevel(0)
    _handle_next_level(curlv, None, fmtr)
    lastlv = curlv
    for i in range(1, adapter.count):
        curlv = adapter.getlevel(i)
        _handle_next_level(curlv, lastlv, fmtr)
        lastlv = curlv
    fdout.write(fmtr.format(True))
    fdout.close()
    return 0


def _handle_next_level(cur, last, formatter):
    if not last:
        formatter.start_new_report([cur])
    else:
        if _colocal(cur, last) and _cotemporal(cur, last):
            formatter.add_level(cur)
        else:
            formatter.start_new_report([cur])


def _colocal(cur, last):
    # XXX: May need to add a tolerance
    return cur.lat == last.lat and cur.lon == last.lat


def _cotemporal(cur, last):
    # XXX: May need to add a tolerance
    return cur.date == last.date
