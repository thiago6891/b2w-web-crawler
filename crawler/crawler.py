from urllib.request import urlopen
from redis import Redis, RedisError

VISITED_URLS_KEY = 'visited_urls'
URLS_TO_VISIT_KEY = 'urls_to_visit'
PROD_PGS_URLS_KEY = 'prod_pgs_urls'

PAGE_TITLE_FIELD = 'page_title'
PROD_NAME_FIELD = 'prod_name'

STARTING_PAGE_URL = 'http://www.epocacosmeticos.com.br/'

redis = Redis(host='redis', db=0, socket_connect_timeout=2, socket_timeout=2)


def _run():
    try:
        url = _get_next_url()

        while url:
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


def _set_url_as_visited(url):
    """Save URL in the visited_urls Set in Redis"""
    redis.sadd(VISITED_URLS_KEY, url)


def _is_response_html(response):
    return 'text/html' in response.getheader('Content-Type')


def _is_product_page(html):
    """Verify if the given HTML is from a product page"""
    # TODO: Implement
    pass


def _add_to_products(url, html):
    """
    Add the URL to the products Set in Redis, and save the product
    name and page title in a Hash with the URL as its key.
    """
    # TODO: Implement
    pass


def _get_inbound_links(html):
    # TODO: Implement
    return []


def _should_visit(url):
    """
    Verify if URL hasn't been visited yet or is it already
    saved in the urls_to_visit Set in Redis
    """
    return (redis.sismember(VISITED_URLS_KEY, url) and
            redis.sismember(URLS_TO_VISIT_KEY, url))


def _add_to_visit(url):
    """Save URL in Redis to be visited later"""
    redis.sadd(URLS_TO_VISIT_KEY, url)


if __name__ == '__main__':
    _run()
