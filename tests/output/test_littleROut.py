from unittest import TestCase

from littler.output.littlerout import _Record, _Report
from littler.level import Level, _DEFAULT_FLOAT


class TestLittleROut(TestCase):

    def test_recordStr(self):
        lv = Level()
        rec = _Record(lv)
        expected_str = '-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0'
        self.assertTrue(str(rec) == expected_str, "Default Record str must match expected")


