from urllib import parse
from urllib.request import urlopen


def _escape_unicode_chars(url):
    """Escape Unicode characters in the URL path"""
    url = list(parse.urlsplit(url))
    url[2] = parse.quote(url[2])
    return parse.urlunsplit(url)


class URLService:
    def __init__(self):
        self._html = None

    @property
    def html(self):
        return self._html

    def open_url(self, url):
        response = urlopen(_escape_unicode_chars(url))
        if 'text/html' in response.getheader('Content-Type'):
            self._html = response.read().decode('utf-8')
        else:
            self._html = None
