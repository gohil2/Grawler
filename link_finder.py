from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    # This function called from HTMLParser , this function is called when encounter opening tags.
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)   # Joins href value part to base_url
                    self.links.add(url)     # Add to links set()

    def page_links(self):
        return self.links

    def error(self, message):
        pass
