import datetime
from unittest import TestCase

from littler.input.adapters import GrawAdapter
from littler.input.level import Level


test_file_count = 4040


class TestGrawAdapter(TestCase):

    def setUp(self):
        with open('../../data/GrawProfile_7_14_SLU.txt', encoding='latin-1') as fd:
            self.now = datetime.datetime.today()
            self.adapter = GrawAdapter(fd, self.now)

    def test_count(self):
        self.assertEqual(self.adapter.count, test_file_count, 'adapter.count must equal data\'s count')

    def test_levels(self):
        self.assertEqual(len(self.adapter.levels), test_file_count, 'adapter.levels must be same length as data')
        self.assertEqual(len(self.adapter.levels), self.adapter.count, 'len(adapter.levels) must equal adapter.count')
        self.assertTrue(all(isinstance(x, Level) for x in self.adapter.levels),
                        'All elements in adapter.levels must be a Level')

    def test_time_string(self):
        test_str = self.now.strftime('%Y%M%d%H%m%S')
        self.assertEqual(self.adapter.getlevel(0).date, test_str, 'Data string must match expected format')

