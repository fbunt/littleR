from littler.level import Level, DEFAULT_FLOAT, DEFAULT_INT

# The contents of this module are implemented using the documentation found at
# http://www2.mmm.ucar.edu/wrf/users/wrfda/OnlineTutorial/Help/littler.html


class LittleRFormatter(object):
    """A class for writing data to a file using the LittleR format.

    LittleR documentation can be found here: http://www2.mmm.ucar.edu/wrf/users/wrfda/OnlineTutorial/Help/littler.html

    LittleR format structure:
    File:
        * Report:
            - Header
            - Record line
            - Record line
            - ...
            - End Record (sentinel)
            - Tail integers
        * Report:
            ...
    """
    def __init__(self):
        self.reports = []

    def start_new_report(self, levels=None):
        r = _Report()
        if levels is not None:
            r.add_records(levels)
        self.reports.append(r)

    def add_level(self, level):
        """Add a new level to the current report.

        'start_new_report' must have been called before this method.
        """
        self.reports[-1].add_record(level)

    def add_levels(self, levels):
        """Add multiple levels"""
        for lv in levels:
            self.add_level(lv)

    def format(self, clear=False):
        """Return all reports formatted into a single string.

        If `clear`, all reports are cleared.
        """
        out = ''.join([str(rep) for rep in self.reports])
        if clear:
            self.clear()
        return out

    def clear(self):
        """Remove all reports"""
        self.reports = []


_END_RECORD_VALUE = -777777.0
# Format string for the tail line of a Report.
# Note: the documentation on the site states that the first integer is the "number of valid
#       fields for the observation", but the actual value seems to be the number of valid
#       records (levels) in the report as seen in MIDAS2LITTLER.
# Number of valid fields (Number of levels), Errors, Warnings
_TAIL_FMT_STR = '{:>7d}'*3


class _Report(object):
    """
    Report Structure:
        * Header line
        * Record line(s)
             ...
        * Ending record line (sentinel values)
        * Tail integers line (Valid "Fields"(records)
    """

    def __init__(self):
        self.records = []
        # Ending sentinel level
        self.ending_lv = Level()
        self.ending_lv.pres = (_END_RECORD_VALUE, 0)
        self.ending_lv.height = (_END_RECORD_VALUE, 0)

    def add_record(self, level):
        self.records.append(_Record(level))

    def add_records(self, levels):
        for lv in levels:
            self.add_record(lv)

    def __str__(self):
        self.add_record(self.ending_lv)
        # Don't include end record
        nrecs = len(self.records) - 1
        header = _Header(self.records[0].lv, nrecs*self.records[0].lv.valid_fields)

        out = [str(header)]
        out.extend([str(r) for r in self.records])
        out.append(_TAIL_FMT_STR.format(nrecs, 0, 0))
        out = '\n'.join(out)
        out += '\n'
        return out


_hf20str = '{:>20.5F}'
_ha40str = '{:<40}'
_ha20str = '{:>20}'
_histr = '{:>10d}'
_hlstr = '{:>10}'
_hfpairstr = '{:>13.5F}{:>7d}'
# Format string for a LittleR Report header
# NOTE: The header section of the documentation site has one more value/QC pair
#       (Precipitable water) at the end of the header def but leaves it out in
#       the example. It is left out here.
_HEADER_FMT_STR = (
    # Lat, Lon
    _hf20str*2
    # ID, Name, Platform, Source
    + _ha40str*4
    # Elevation
    + _hf20str
    # Valid Fields, Num Errors, Num Warnings, Sequence Num, Num duplicates
    + _histr*5
    # Is Sounding?, Is Bogus?, Discard?
    + _hlstr*3
    # Unix Time, Julian Day
    + _histr*2
    # Date
    + _ha20str
    # SLP, Ref Press, Ground Temp, SST, SFC Press, Precip, Daily Max, Daily Min, Night Min,
    # 3hr Press Change, 24hr Press Change, Cloud Cover, Ceiling
    + _hfpairstr*13
)


class _Header(object):
    def __init__(self, level, valid_fields):
        self.lv = level
        self.valid_fields = valid_fields

    def __str__(self):
        lv = self.lv
        # See above for fields
        args = [lv.lat, lv.lon]
        args.extend([lv.id[:40], lv.name[:40], lv.platform[:40], lv.source[:40]])
        args.append(lv.alt)
        args.extend([self.valid_fields, DEFAULT_INT, DEFAULT_INT, lv.seq_num, DEFAULT_INT])
        args.extend([_b_to_str(lv.is_sounding), _b_to_str(lv.bogus), _b_to_str(False)])
        args.extend([DEFAULT_INT, DEFAULT_INT])
        args.append(lv.date[:40])
        args.extend([lv.slp[0], 0])
        args.extend([DEFAULT_FLOAT, 0]*3)
        args.extend([lv.sfc_pres[0], 0])
        args.extend([DEFAULT_FLOAT, 0]*8)
        return _HEADER_FMT_STR.format(*args)


def _b_to_str(b):
    if b:
        return 'T'
    else:
        return 'F'


# Format string for a LittleR level Record.
# Fields: Press, Height, Temp, Dew Point, Wind Spd, Wind Dir, Wind U, Wind V, Rel. Humidity, Thickness
_RECORD_FMT_STR = '{:13.5F}{:7d}'*10


class _Record(object):
    def __init__(self, level):
        self.lv = level

    def __str__(self):
        lv = self.lv
        args = []
        args.extend(lv.pres)
        args.extend(lv.height)
        args.extend(lv.temp)
        args.extend(lv.dewpoint)
        args.extend(lv.windspd)
        args.extend(lv.winddir)
        args.extend(lv.windu)
        args.extend(lv.windv)
        args.extend(lv.rh)
        args.extend(lv.thickness)
        return _RECORD_FMT_STR.format(*args)
