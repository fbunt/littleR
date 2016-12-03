from unittest import TestCase

import os

from littler.adapters import GrawAdapter


class TestGrawAdapter(TestCase):

    def setUp(self):
        with open('../data/GrawProfile_7_14_SLU.txt', encoding='latin-1') as fd:
            self.adapter = GrawAdapter(fd)

    def test_count(self):
        self.assertEqual(self.adapter.count, 4040)


