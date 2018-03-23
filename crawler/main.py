from .crawler import Crawler
from .db_service import DBService
from .url_service import URLService
from .html_service import HTMLService

if __name__ == '__main__':
    Crawler(DBService(), URLService(), HTMLService()).crawl()
