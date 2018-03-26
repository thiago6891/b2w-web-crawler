from html.parser import HTMLParser
from urllib import parse


class InboundLinkParser(HTMLParser):
    def __init__(self, base_url):
        super(InboundLinkParser, self).__init__()
        self._base_url = base_url
        self._links = []

    @property
    def links(self):
        return self._links

    def handle_starttag(self, tag, attributes):
        if tag == 'a':
            for key in attributes:
                if key[0] == 'href':
                    url = parse.urljoin(self._base_url, key[1])

                    # Make sure it's an inbound link
                    if parse.urlparse(self._base_url).netloc in url:
                        self._links.append(url)
