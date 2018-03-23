import os
from urllib import parse
from urllib.request import urlopen
from .product_page_parser import ProductPageParser
from .link_parser import InboundLinkParser

STARTING_PAGE_URL = os.getenv('STARTING_PAGE_URL')
PAGE_KW = os.getenv('PAGE_KW')

# <---------- BEGIN Helper methods ---------->


def _escape_unicode_chars(url):
    """Escape Unicode characters in the URL path"""
    url = list(parse.urlsplit(url))
    url[2] = parse.quote(url[2])
    return parse.urlunsplit(url)


def _is_response_html(response):
    return 'text/html' in response.getheader('Content-Type')


def _is_product_page(html):
    """Verify if the given HTML is from a product page"""
    return PAGE_KW in html


def _get_product_page_info(html):
    parser = ProductPageParser()
    parser.feed(html)
    return parser.page_title, parser.product_name


def _get_inbound_links(html):
    parser = InboundLinkParser(STARTING_PAGE_URL)
    parser.feed(html)
    return parser.links


# <---------- END Helper methods ---------->


class Crawler:
    def __init__(self, db_service):
        self._db_service = db_service
        self._url = None

    def crawl(self):
        while self._prepare_next_url():
            response = urlopen(self._url)
            # Set the URL as visited so the crawler won't visit it again
            self._db_service.set_url_visited(self._url)

            if _is_response_html(response):
                html = response.read().decode('utf-8')

                # If it's a product page, save it in the DB
                if _is_product_page(html):
                    page_title, product_name = _get_product_page_info(html)
                    self._db_service.add_product(self._url,
                                                 page_title,
                                                 product_name)

                # Get the links from the page and save
                # the ones that haven't been visited yet
                links = _get_inbound_links(html)
                for link in links:
                    if not self._db_service.is_url_visited(link):
                        self._db_service.set_url_to_visit(link)

    def _prepare_next_url(self):
        """
        Gets the next URL to visit and prepares it to be visited by
        escaping invalid characters.
        :return: True if a URL was retrieved, False otherwise.
        """
        url = self._db_service.get_next_url_to_visit()
        if url:
            self._url = _escape_unicode_chars(url.decode('utf-8'))
            return True
        else:
            return False
