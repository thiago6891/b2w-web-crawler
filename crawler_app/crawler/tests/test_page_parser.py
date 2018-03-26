import unittest
from ..product_page_parser import ProductPageParser


def _create_html(product_name, page_title):
    name_tag = ''
    title_tag = ''

    if product_name:
        name_tag = '<meta property="og:title" content="{}"></meta>'.format(
            product_name)
    if page_title:
        title_tag = '<title>{}</title>'.format(page_title)

    return '<head>{}{}</head>'.format(name_tag, title_tag)


class TestPageParser(unittest.TestCase):
    def setUp(self):
        self._parser = ProductPageParser()

    def _test(self, product_name, page_title):
        html = _create_html(product_name, page_title)

        self._parser.feed(html)

        self.assertEqual(self._parser.product_name, product_name)
        self.assertEqual(self._parser.page_title, page_title)

    def test_missing_product_page_and_page_title(self):
        self._test('', '')

    def test_product_page(self):
        self._test('product_name', 'page_title')

    def test_missing_product_name(self):
        self._test('', 'page_title')

    def test_missing_page_title(self):
        self._test('product_name', 'page_title')
