from unittest import TestCase

from littler.input import parse_meta_data, MetaDataParsingError

from tests.utils import get_data_filename, MyStringIO


# Header examples with missing fields
bad_headers_missing = [
    '---date: 02/03/2017\nstart time: 19:48:02\nsource: UAV flight MREDI\n...',
    '---\nid: 1234\nstart time: 19:48:02\nsource: UAV flight MREDI\n...'
    '---id: 123\ndate: 02/03/2017\nsource: UAV flight MREDI\n...',
    '---id: 123\ndate: 02/03/2017\nstart time: 19:48:02\n...'
    '---...',
    ''
]
bad_headers_invalid_fields = [
    '---id: 123\ndate: 02//2017\nstart time: 19:48:02\nsource: UAV flight MREDI\n...',
    '---id: 123\ndate: 02/03/17\nstart time: 19:48:02\nsource: UAV flight MREDI\n...',
    '---id: 123\ndate: \nstart time: 19:48:02\nsource: UAV flight MREDI\n...'
    '---id: 123\ndate: 02/03/2017\nstart time: 19:48:\nsource: UAV flight MREDI\n...',
    '---id: 123\ndate: 02/03/2017\nstart time: 19:4802\nsource: UAV flight MREDI\n...',
    '---id: 123\ndate: 02/03/2017\nstart time: \nsource: UAV flight MREDI\n...',
    '---id: 123\ndate: 02/03/2017\nstart time: 19:48:02\nsource:\n...',
    '---id: \ndate: \nstart time: \nsource:\n...'
]


class TestMetaDataParser(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fd = open(get_data_filename('02032017SUAT_UAVflight_MREDI_19.48.02.txt'))

    @classmethod
    def tearDownClass(cls):
        cls.fd.close()

    def setUp(self):
        self.fd.seek(0)

    def test_parse_data(self):
        data = parse_meta_data(self.fd)

        self.assertEqual(4, len(data))
        self.assertEqual('1234', data[0])
        self.assertEqual('UAV flight MREDI', data[1])
        self.assertEqual('02032017SUAT_UAVflight_MREDI_19.48.02', data[2])
        dt = data[3]
        self.assertEqual(dt.year, 2017)
        self.assertEqual(dt.month, 2)
        self.assertEqual(dt.day, 3)
        self.assertEqual(dt.hour, 19)
        self.assertEqual(dt.minute, 48)
        self.assertEqual(dt.second, 2)

    def test_parse_file_location(self):
        # Make sure that the parser doesn't read farther than it needs to
        data = parse_meta_data(self.fd)

        line = self.fd.readline().replace('\r\n', '\n')
        self.assertEqual('Flight Information:\n', line)

    def test_parse_no_header(self):
        noheadfd = open(get_data_filename('GrawProfile_7_14_SLU.txt'))
        self.assertRaises(MetaDataParsingError, parse_meta_data, noheadfd)
        noheadfd.close()

    def test_parse_bad_header(self):
        for h in bad_headers_missing:
            with MyStringIO(h) as fd:
                self.assertRaises(MetaDataParsingError, parse_meta_data, fd)

        for h in bad_headers_invalid_fields:
            with MyStringIO(h) as fd:
                self.assertRaises(MetaDataParsingError, parse_meta_data, fd)
