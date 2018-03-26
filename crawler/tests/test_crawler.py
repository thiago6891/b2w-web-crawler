import unittest
from unittest.mock import MagicMock, call
from ..crawler import Crawler


def get_next_url_mock(urls):
    try:
        return urls.pop()
    except IndexError:
        return None


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self._url = 'https://www.epocacosmeticos.com.br/'
        self._urls = [self._url.encode('utf-8')]

        self._db = MagicMock()
        self._db.get_next_url_to_visit = self._urls.pop
        self._db.set_url_visited = MagicMock()
        self._db.add_product = MagicMock()
        self._db.is_url_visited = MagicMock(return_value=True)
        self._db.set_url_to_visit = MagicMock()

        self._url_service = MagicMock()
        self._url_service.open_url = MagicMock()

        self._html_service = MagicMock()
        self._html_service.set_html = MagicMock()
        self._html_service.is_product_page = MagicMock(return_value=True)
        self._html_service.get_product_page_info = MagicMock(return_value=[
            'page title',
            'product name'])
        self._html_service.get_links = MagicMock(return_value=[
            'link1',
            'link2'])

    def tearDown(self):
        self._url = None
        self._urls = None
        self._db = None
        self._url_service = None
        self._html_service = None

    def test_visit_product_page(self):
        crawler = Crawler(self._db, self._url_service, self._html_service)
        try:
            crawler.crawl()
        except IndexError:
            # Ignore IndexError, there are no more URLs to visit
            pass

        self._url_service.open_url.assert_called_once_with(self._url)
        self._db.set_url_visited.assert_called_once_with(self._url)
        self._html_service.is_product_page.assert_called_once_with()
        self._html_service.get_product_page_info.assert_called_once_with()
        self._db.add_product.assert_called_once_with(self._url,
                                                     'page title',
                                                     'product name')
        self._html_service.get_links.assert_called_once_with()
        self._db.is_url_visited.assert_has_calls([
            call('link1'),
            call('link2')])
        self._db.set_url_to_visit.assert_not_called()

    def test_visit_non_product_page(self):
        self._html_service.is_product_page = MagicMock(return_value=False)

        crawler = Crawler(self._db, self._url_service, self._html_service)
        try:
            crawler.crawl()
        except IndexError:
            # Ignore IndexError, there are no more URLs to visit
            pass

        self._url_service.open_url.assert_called_once_with(self._url)
        self._db.set_url_visited.assert_called_once_with(self._url)
        self._html_service.is_product_page.assert_called_once_with()
        self._html_service.get_product_page_info.assert_not_called()
        self._db.add_product.assert_not_called()
        self._html_service.get_links.assert_called_once_with()
        self._db.is_url_visited.assert_has_calls([
            call('link1'),
            call('link2')])
        self._db.set_url_to_visit.assert_not_called()

    def test_add_unvisited_links(self):
        self._db.is_url_visited = MagicMock(return_value=False)

        crawler = Crawler(self._db, self._url_service, self._html_service)
        try:
            crawler.crawl()
        except IndexError:
            # Ignore IndexError, there are no more URLs to visit
            pass

        self._url_service.open_url.assert_called_once_with(self._url)
        self._db.set_url_visited.assert_called_once_with(self._url)
        self._html_service.is_product_page.assert_called_once_with()
        self._html_service.get_product_page_info.assert_called_once_with()
        self._db.add_product.assert_called_once_with(self._url,
                                                     'page title',
                                                     'product name')
        self._html_service.get_links.assert_called_once_with()
        self._db.is_url_visited.assert_has_calls([
            call('link1'),
            call('link2')])
        self._db.set_url_to_visit.assert_has_calls([
            call('link1'),
            call('link2')
        ])

    def test_no_links_in_page(self):
        self._html_service.get_links = MagicMock(return_value=[])

        crawler = Crawler(self._db, self._url_service, self._html_service)
        try:
            crawler.crawl()
        except IndexError:
            # Ignore IndexError, there are no more URLs to visit
            pass

        self._url_service.open_url.assert_called_once_with(self._url)
        self._db.set_url_visited.assert_called_once_with(self._url)
        self._html_service.is_product_page.assert_called_once_with()
        self._html_service.get_product_page_info.assert_called_once_with()
        self._db.add_product.assert_called_once_with(self._url,
                                                     'page title',
                                                     'product name')
        self._html_service.get_links.assert_called_once_with()
        self._db.is_url_visited.assert_not_called()
        self._db.set_url_to_visit.assert_not_called()

    def test_no_urls_to_visit(self):
        self._urls = []
        self._db.get_next_url_to_visit = self._urls.pop

        crawler = Crawler(self._db, self._url_service, self._html_service)
        try:
            crawler.crawl()
        except IndexError:
            # Ignore IndexError, there are no more URLs to visit
            pass

        self._url_service.open_url.assert_not_called()
        self._db.set_url_visited.assert_not_called()
        self._html_service.is_product_page.assert_not_called()
        self._html_service.get_product_page_info.assert_not_called()
        self._db.add_product.assert_not_called()
        self._html_service.get_links.assert_not_called()
        self._db.is_url_visited.assert_not_called()
        self._db.set_url_to_visit.assert_not_called()
