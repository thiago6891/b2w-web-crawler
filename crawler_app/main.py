from crawler.crawler import Crawler
from crawler.db_service import DBService
from crawler.url_service import URLService
from crawler.html_service import HTMLService

if __name__ == '__main__':
    Crawler(DBService(), URLService(), HTMLService()).crawl()
