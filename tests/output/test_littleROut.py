from unittest import TestCase

from littler.output.littlerout import _Record, _Report
from littler.level import Level, _DEFAULT_FLOAT


class TestLittleROut(TestCase):

    def test_recordStr(self):
        lv = Level()
        rec = _Record(lv)
        expected_str = '-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0'
        self.assertEqual(str(rec), expected_str, "Default Record str must match expected")

        lv = Level()
        lv.pres = (83500.00000, 0)
        lv.temp = (264.44998, 0)
        lv.dewpoint = (263.35001, 0)
        rec = _Record(lv)
        expected_str = '  83500.00000      0-888888.00000      0    264.44998      0    263.35001      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0'
        self.assertEqual(str(rec), expected_str, "Record str must match expected")



