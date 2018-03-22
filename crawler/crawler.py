from urllib import parse
from urllib.request import urlopen
from redis import Redis, RedisError
from product_page_parser import ProductPageParser
from link_parser import InboundLinkParser

VISITED_URLS_KEY = 'visited_urls'
URLS_TO_VISIT_KEY = 'urls_to_visit'
PROD_PGS_URLS_KEY = 'prod_pgs_urls'

PAGE_TITLE_FIELD = 'page_title'
PROD_NAME_FIELD = 'prod_name'

STARTING_PAGE_URL = 'https://www.epocacosmeticos.com.br/'

PAGE_KW = 'og:product'

redis = Redis(host='redis', db=0, socket_connect_timeout=2, socket_timeout=2)


def _run():
    try:
        url = _get_next_url()

        while url:
            url = url.decode('utf-8')
            url = _escape_unicode_chars(url)
            response = urlopen(url)

            _set_url_as_visited(url)

            if _is_response_html(response):
                html = response.read().decode('utf-8')

                if _is_product_page(html):
                    _add_to_products(url, html)

                links = _get_inbound_links(html)

                for link in links:
                    if _should_visit(link):
                        _add_to_visit(link)

            url = _get_next_url()
    except RedisError:
        # Let the crawler crash and Docker will handle reinitialization
        raise


def _get_next_url():
    """Get a random URL to visit"""
    return redis.spop(URLS_TO_VISIT_KEY)


def _escape_unicode_chars(url):
    """Escape Unicode characters in the URL path"""
    url = list(parse.urlsplit(url))
    url[2] = parse.quote(url[2])
    return parse.urlunsplit(url)


def _set_url_as_visited(url):
    """Save URL in the visited_urls Set in Redis"""
    redis.sadd(VISITED_URLS_KEY, url)


def _is_response_html(response):
    return 'text/html' in response.getheader('Content-Type')


def _is_product_page(html):
    """Verify if the given HTML is from a product page"""
    return PAGE_KW in html


def _add_to_products(url, html):
    """
    Add the URL to the products Set in Redis, and save the product
    name and page title in a Hash with the URL as its key.
    """
    parser = ProductPageParser()
    parser.feed(html)

    redis.sadd(PROD_PGS_URLS_KEY, url)
    redis.hset(url, PAGE_TITLE_FIELD, parser.page_title)
    redis.hset(url, PROD_NAME_FIELD, parser.product_name)


def _get_inbound_links(html):
    parser = InboundLinkParser(STARTING_PAGE_URL)
    parser.feed(html)
    return parser.links


def _should_visit(url):
    """
    Verify if URL hasn't been visited yet nor already
    saved in the urls_to_visit Set in Redis
    """
    return (not redis.sismember(VISITED_URLS_KEY, url) and
            not redis.sismember(URLS_TO_VISIT_KEY, url))


def _add_to_visit(url):
    """Save URL in Redis to be visited later"""
    redis.sadd(URLS_TO_VISIT_KEY, url)


if __name__ == '__main__':
    _run()
