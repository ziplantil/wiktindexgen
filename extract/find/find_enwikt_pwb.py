
import datetime
import wikitextlib
from pywikibot import Site, Page, Category

class Finder():
    def __init__(self, args, kwargs):
        self.site = Site("en", fam="wiktionary")
        self.site.login()
        self.category = Category(self.site, l2 + " lemmas")

    def get_date(self):
        return datetime.datetime.now().date().isoformat()

    def get_pages(self, l2):
        catlist = self.site.preloadpages(self.category.articles())
        while True:
            try:
                page = next(catlist)
            except StopIteration:
                break
            title = page.title()
            text = page.text
            if wikitextlib.contains_l2(text, l2):
                yield (title, wikitextlib.get_section_text(text, 2, l2))
