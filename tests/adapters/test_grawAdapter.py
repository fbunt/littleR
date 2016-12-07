from unittest import TestCase

import os

from littler.adapters import GrawAdapter, Level

test_file_count = 4040


class TestGrawAdapter(TestCase):

    def setUp(self):
        with open('../data/GrawProfile_7_14_SLU.txt', encoding='latin-1') as fd:
            self.adapter = GrawAdapter(fd)

    def test_count(self):
        self.assertEqual(self.adapter.count, test_file_count, 'adapter.count must equal data\'s count')

    def test_levels(self):
        self.assertEqual(len(self.adapter.levels), test_file_count, 'adapter.levels must be same length as data')
        self.assertEqual(len(self.adapter.levels), self.adapter.count, 'len(adapter.levels) must equal adapter.count')
        self.assertTrue(all(isinstance(x, Level) for x in self.adapter.levels),
                        'All elements in adapter.levels must be a Level')

