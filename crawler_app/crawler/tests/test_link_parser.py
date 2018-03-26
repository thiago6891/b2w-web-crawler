import unittest
from ..link_parser import InboundLinkParser


def _create_html(href):
    return '<body><a href="{}">Text</a><body>'.format(href)


class TestLinkParser(unittest.TestCase):
    def setUp(self):
        self._base_url = 'https://www.google.com'
        self._parser = InboundLinkParser(self._base_url)

    def test_parse_relative(self):
        href = '/test_relative'
        self._parser.feed(_create_html(href))

        self.assertListEqual(self._parser.links, [self._base_url + href])

    def test_parse_absolute(self):
        href = self._base_url + '/test_absolute'
        self._parser.feed(_create_html(href))

        self.assertListEqual(self._parser.links, [href])

    def test_parse_only_inbound(self):
        href = 'https://www.outboundurl.com/whatever'
        self._parser.feed(_create_html(href))

        self.assertListEqual(self._parser.links, [])
