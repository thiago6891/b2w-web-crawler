import os

STARTING_PAGE_URL = os.getenv('STARTING_PAGE_URL')
PAGE_KW = os.getenv('PAGE_KW')


class Crawler:
    def __init__(self, db_service, url_service, html_service):
        self._db_service = db_service
        self._url_service = url_service
        self._html_service = html_service
        self._url = None

    def crawl(self):
        while self._prepare_next_url():
            self._url_service.open_url(self._url)
            # Set the URL as visited so the crawler won't visit it again
            self._db_service.set_url_visited(self._url)

            html = self._url_service.html
            if html:
                self._html_service.set_html(html)

                # If it's a product page, save it in the DB
                if self._html_service.is_product_page():
                    page_title, product_name = \
                        self._html_service.get_product_page_info()
                    self._db_service.add_product(self._url,
                                                 page_title,
                                                 product_name)

                # Get the links from the page and save
                # the ones that haven't been visited yet
                links = self._html_service.get_links()
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
            self._url = url.decode('utf-8')
            return True
        else:
            return False
