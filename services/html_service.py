import os
from crawler.product_page_parser import ProductPageParser
from crawler.link_parser import InboundLinkParser

PAGE_KW = os.getenv('PAGE_KW')
STARTING_PAGE_URL = os.getenv('STARTING_PAGE_URL')


class HTMLService:
    def __init__(self):
        self._html = None

    def set_html(self, html):
        self._html = html

    def is_product_page(self):
        """Verify if the given HTML is from a product page"""
        return PAGE_KW in self._html

    def get_product_page_info(self):
        parser = ProductPageParser()
        parser.feed(self._html)
        return parser.page_title, parser.product_name

    def get_links(self):
        parser = InboundLinkParser(STARTING_PAGE_URL)
        parser.feed(self._html)
        return parser.links
