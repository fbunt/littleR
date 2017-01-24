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


