from .crawler import Crawler
from .db_service import DBService

if __name__ == '__main__':
    Crawler(DBService()).crawl()
