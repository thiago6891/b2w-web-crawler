from crawler.crawler import Crawler
from services.db_service import DBService
from services.html_service import HTMLService
from services.url_service import URLService

if __name__ == '__main__':
    Crawler(DBService(), URLService(), HTMLService()).crawl()
