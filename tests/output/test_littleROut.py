from unittest import TestCase

from littler.output.littlerout import _Record, _Header, _Report
from littler.level import Level, DEFAULT_FLOAT


class TestLittleROut(TestCase):

    def test_recordStr(self):
        # Test default
        lv = Level()
        rec = _Record(lv)
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
        lv.lat = 39.78000
        lv.lon = -104.86000
        lv.id = '72469'
        lv.name = 'DENVER/STAPLETON INT., CO. / U.S.A.'
        lv.platform = 'FM-35 TEMP'
        lv.source = 'GTS (ROHK) UKUS09 KWBC 051200 RRA'
        lv.alt = 1626.00000
        lv.valid_fields = 1
        lv.seq_num = 890
        lv.is_sounding = True
        lv.bogus = False
        lv.date = '20080205120000'

        header = _Header(lv, lv.valid_fields)
        expected_str = '            39.78000          -104.8600072469                                   DENVER/STAPLETON INT., CO. / U.S.A.     FM-35 TEMP                              GTS (ROHK) UKUS09 KWBC 051200 RRA                 1626.00000         1   -888888   -888888       890   -888888         T         F         F   -888888   -888888      20080205120000-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0'
        self.assertEqual(str(header), expected_str)

    def test_reportStr(self):
        # Taken from http://www2.mmm.ucar.edu/wrf/users/wrfda/OnlineTutorial/Help/littler.html
        lines = [
            '  83500.00000      0-888888.00000      0    264.44998      0    263.35001      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0',
            '  72100.00000      0-888888.00000      0    257.85001      0    256.14999      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0',
            '  59100.00000      0-888888.00000      0    252.45000      0    250.34999      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0',
            '  46600.00000      0-888888.00000      0    241.84999      0    239.34999      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0',
            '  40000.00000      0-888888.00000      0    232.84999      0    229.75000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0',
            '  37200.00000      0-888888.00000      0    229.84999      0    223.84999      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0',
            '  33900.00000      0-888888.00000      0    228.04999      0    214.04999      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0',
            '  25400.00000      0-888888.00000      0    226.45000      0    202.45000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0',
            '  23300.00000      0-888888.00000      0    229.45000      0    201.45000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0',
            '  14100.00000      0-888888.00000      0    220.64999      0    195.64999      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0',
            '  10000.00000      0-888888.00000      0    218.64999      0    194.64999      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0'
        ]
        levels = [_str_to_level(line) for line in lines]
        rep = _Report()
        rep.add_records(levels)
        expected_str = 'TODO'
        print(rep)
        self.assertEqual(str(rep), expected_str, 'Report str must match expected')


def _str_to_level(s):
    n = 20
    tmp = [s[i*n:i*n + n] for i in range(len(s) // 20)]
    vals = []
    for t in tmp:
        vals.append(float(t.split()[0]))

    lv = Level()
    lv.valid_fields = vals.count(DEFAULT_FLOAT)
    lv.pres = (vals[0], 0)
    lv.height = (vals[1], 0)
    lv.temp = (vals[2], 0)
    lv.dewpoint = (vals[2], 0)
    lv.windspd = (vals[2], 0)
    lv.winddir = (vals[2], 0)
    lv.windu = (vals[2], 0)
    lv.windv = (vals[2], 0)
    lv.rh = (vals[2], 0)
    lv.thickness = (vals[2], 0)
    return lv


