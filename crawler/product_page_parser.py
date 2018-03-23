from html.parser import HTMLParser


class ProductPageParser(HTMLParser):
    def __init__(self):
        super(ProductPageParser, self).__init__()
        self._page_title = ''
        self._product_name = ''
        self._accessing_page_title = False

    @property
    def page_title(self):
        return self._page_title

    @property
    def product_name(self):
        return self._product_name

    def handle_starttag(self, tag, attributes):
        if tag == 'meta':
            found_product_name_tag = False

            # Looking for <meta property="og:title" content="...
            for key in attributes:
                if key[0] == 'property' and key[1] == 'og:title':
                    found_product_name_tag = True

            if found_product_name_tag:
                for key in attributes:
                    if key[0] == 'content':
                        self._product_name = key[1]

        elif tag == 'title':
            self._accessing_page_title = True

    def handle_data(self, data):
        if self._accessing_page_title:
            self._page_title = data

    def handle_endtag(self, tag):
        if tag == 'title' and self._accessing_page_title:
            self._accessing_page_title = False
