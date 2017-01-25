from unittest import TestCase

from littler.output.littlerout import _Record, _Header, _Report
from littler.level import Level, DEFAULT_FLOAT


class TestLittleROut(TestCase):

    def test_recordStr(self):
        # Test default
        rec = _Record(Level())

        expected_str = '-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0'
        self.assertEqual(str(rec), expected_str, "Default Record str must match expected")

        # Test with specific values
        lv = Level()
        lv.pres = (83500.00000, 0)
        lv.temp = (264.44998, 0)
        lv.dewpoint = (263.35001, 0)
        rec = _Record(lv)

        expected_str = '  83500.00000      0-888888.00000      0    264.44998      0    263.35001      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0'
        self.assertEqual(str(rec), expected_str, "Record str must match expected")

    def test_headerStr(self):
        lv = Level()
        _set_header_vals(lv)
        lv.valid_fields = 1
        header = _Header(lv, lv.valid_fields)

        expected_str = '            39.78000          -104.8600072469                                   DENVER/STAPLETON INT., CO. / U.S.A.     FM-35 TEMP                              GTS (ROHK) UKUS09 KWBC 051200 RRA                 1626.00000         1   -888888   -888888       890   -888888         T         F         F   -888888   -888888      20080205120000-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0'
        self.assertEqual(str(header), expected_str)

    def test_reportStr(self):
        # Taken from http://www2.mmm.ucar.edu/wrf/users/wrfda/OnlineTutorial/Help/littler.html
        levels = [
            [83500.0, -888888.0, 264.44998, 263.35001, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0],
            [72100.0, -888888.0, 257.85001, 256.14999, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0],
            [59100.0, -888888.0, 252.45000, 250.34999, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0],
            [46600.0, -888888.0, 241.84999, 239.34999, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0],
            [40000.0, -888888.0, 232.84999, 229.75000, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0],
            [37200.0, -888888.0, 229.84999, 223.84999, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0],
            [33900.0, -888888.0, 228.04999, 214.04999, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0],
            [25400.0, -888888.0, 226.45000, 202.45000, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0],
            [23300.0, -888888.0, 229.45000, 201.45000, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0],
            [14100.0, -888888.0, 220.64999, 195.64999, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0],
            [10000.0, -888888.0, 218.64999, 194.64999, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0, -888888.0]
        ]
        levels = [_vals_to_level(lv) for lv in levels]
        rep = _Report()
        rep.add_records(levels)

        with open('../data/ExampleReport.txt') as fd:
            expected_str = ''.join(fd.readlines())
        self.assertEqual(str(rep), expected_str, 'Report str must match expected')


def _vals_to_level(vals):
    lv = Level()
    _set_header_vals(lv)
    lv.valid_fields = len(vals) - vals.count(DEFAULT_FLOAT)
    lv.pres = (vals[0], 0)
    lv.height = (vals[1], 0)
    lv.temp = (vals[2], 0)
    lv.dewpoint = (vals[3], 0)
    lv.windspd = (vals[4], 0)
    lv.winddir = (vals[5], 0)
    lv.windu = (vals[6], 0)
    lv.windv = (vals[7], 0)
    lv.rh = (vals[8], 0)
    lv.thickness = (vals[9], 0)
    return lv


def _set_header_vals(lv):
    lv.lat = 39.78000
    lv.lon = -104.86000
    lv.id = '72469'
    lv.name = 'DENVER/STAPLETON INT., CO. / U.S.A.'
    lv.platform = 'FM-35 TEMP'
    lv.source = 'GTS (ROHK) UKUS09 KWBC 051200 RRA'
    lv.alt = 1626.00000
    lv.seq_num = 890
    lv.is_sounding = True
    lv.bogus = False
    lv.date = '20080205120000'
