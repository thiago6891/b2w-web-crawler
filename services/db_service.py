import os
from redis import Redis

VISITED_URLS_KEY = os.getenv('VISITED_URLS_KEY')
URLS_TO_VISIT_KEY = os.getenv('URLS_TO_VISIT_KEY')
PROD_PGS_URLS_KEY = os.getenv('PROD_PGS_URLS_KEY')
PAGE_TITLE_FIELD = os.getenv('PAGE_TITLE_FIELD')
PROD_NAME_FIELD = os.getenv('PROD_NAME_FIELD')
REDIS_HOST = os.getenv('REDIS_HOST')


class DBService:
    def __init__(self):
        self._db = Redis(REDIS_HOST)

    def total_products_count(self):
        """Return the count of saved products in DB"""
        return self._db.scard(PROD_PGS_URLS_KEY)

    def total_visited_urls(self):
        """Return the count of visited URLs"""
        return self._db.scard(VISITED_URLS_KEY)

    def total_urls_to_visit(self):
        """Return the count of URLs to visit"""
        return self._db.scard(URLS_TO_VISIT_KEY)

    def get_all_product_urls(self):
        """Return a list with all product URLs found so far"""
        return self._db.smembers(PROD_PGS_URLS_KEY)

    def get_page_title(self, url):
        """Return the page title of the given URL"""
        return self._db.hget(url, PAGE_TITLE_FIELD)

    def get_product_name(self, url):
        """Return the product name of the given URL"""
        return self._db.hget(url, PROD_NAME_FIELD)

    def get_next_url_to_visit(self):
        """Get a random URL to visit"""
        return self._db.spop(URLS_TO_VISIT_KEY)

    def add_product(self, url, page_title, product_name):
        """
        Add the URL to the products Set in Redis, and save the product
        name and page title in a Hash with the URL as its key.
        """
        self._db.sadd(PROD_PGS_URLS_KEY, url)
        self._db.hset(url, PAGE_TITLE_FIELD, page_title)
        self._db.hset(url, PROD_NAME_FIELD, product_name)

    def set_url_visited(self, url):
        """Save URL in the visited_urls Set in Redis"""
        self._db.sadd(VISITED_URLS_KEY, url)

    def set_url_to_visit(self, url):
        """Save URL in Redis to be visited later"""
        self._db.sadd(URLS_TO_VISIT_KEY, url)

    def is_url_visited(self, url):
        return self._db.sismember(VISITED_URLS_KEY, url)
