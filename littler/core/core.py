from littler.output import LittleRFormatter


class LittleRError(Exception):
    pass


class Core:
    def __init__(self, adapter, fdout):
        self.out = fdout
        self.adapter = adapter
        self.fmtr = LittleRFormatter()

    def run(self):
        if self.adapter.count <= 0:
            raise LittleRError('No data found. Level count: ' + str(self.adapter.count))

        curlv = self.adapter.get(0)
        self._handle_next_level(curlv, None)
        lastlv = curlv
        for i in range(1, self.adapter.count):
            curlv = self.adapter.get(i)
            self._handle_next_level(curlv, lastlv)
            lastlv = curlv
        self.out.write(self.fmtr.format(True))
        self.out.close()

    def _handle_next_level(self, cur, last):
        if not last:
            self.fmtr.start_new_report([cur])
        else:
            if _colocal(cur, last) and _cotemporal(cur, last):
                self.fmtr.add_level(cur)
            else:
                self.fmtr.start_new_report([cur])


def _colocal(cur, last):
    # XXX: May need to add a tolerance
    return cur.lat == last.lat and cur.lon == last.lat


def _cotemporal(cur, last):
    # XXX: May need to add a tolerance
    return cur.date == last.date
