class LittleROut:
    def __init_(self, dst_filename):
        self.reports = []
        self.out = open(dst_filename, 'w', encoding='ascii')

    def start_new_report(self, header, levels=None):
        r = _Report(header)
        if levels is not None:
            r.add_records(levels)
        self.reports.append(r)

    def add_level(self, level):
        self.reports[-1].add_record(level)


class _Report:
    def __init__(self, header):
        self.header = header
        self.records = []

    def add_record(self, level):
        self.records.append(_Record(level))

    def add_records(self, levels):
        for lv in levels:
            self.records.append(_Record(lv))

    def __str__(self):
        # TODO: implement
        return ''


_RECORD_FMT_STR = '{:13.5F}{:7d}'*10


class _Record:
    def __init__(self, level):
        self.lv = level

    def __str__(self):
        return _RECORD_FMT_STR.format(*self.lv.pres,
                                     *self.lv.height,
                                     *self.lv.temp,
                                     *self.lv.dewpoint,
                                     *self.lv.windspd,
                                     *self.lv.winddir,
                                     *self.lv.windu,
                                     *self.lv.windv,
                                     *self.lv.rh,
                                     *self.lv.thickness)
